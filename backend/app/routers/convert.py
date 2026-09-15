import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ..extract import index_files, safe_extract
from ..formats import coco, detect_and_parse, voc, yolo

router = APIRouter(prefix="/convert", tags=["convert"])

TARGETS = {"yolo", "coco", "voc"}


@router.post("")
async def convert(file: UploadFile = File(...), target: str = Form(...)):
    if target not in TARGETS:
        raise HTTPException(400, f"Target must be one of {sorted(TARGETS)}")
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(400, "Upload a .zip archive")

    work = Path(tempfile.mkdtemp(prefix="labellint_conv_"))
    try:
        zip_path = work / "in.zip"
        with open(zip_path, "wb") as out:
            shutil.copyfileobj(file.file, out)

        extracted = work / "in"
        safe_extract(zip_path, extracted)
        images, annotations = index_files(extracted)

        if not images:
            raise HTTPException(400, "No images found in the archive")

        ds = detect_and_parse(extracted, images, annotations)

        if ds.source_format == target:
            raise HTTPException(400, f"Dataset is already in {target} format")
        if ds.source_format == "images-only":
            raise HTTPException(400, "No annotations found to convert")

        out_dir = work / "out"
        out_dir.mkdir()

        if target == "yolo":
            yolo.write(ds, out_dir)
        elif target == "coco":
            coco.write(ds, out_dir / "annotations.json")
        else:
            voc.write(ds, out_dir / "annotations")

        archive = shutil.make_archive(str(work / "converted"), "zip", out_dir)
        return FileResponse(
            archive,
            media_type="application/zip",
            filename=f"{target}-annotations.zip",
        )
    except HTTPException:
        shutil.rmtree(work, ignore_errors=True)
        raise
    except Exception as e:
        shutil.rmtree(work, ignore_errors=True)
        raise HTTPException(400, f"Conversion failed: {e}")