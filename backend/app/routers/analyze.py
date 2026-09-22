import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from ..checks import run_all
from ..config import settings
from ..extract import ExtractionError, index_files, safe_extract
from ..formats import detect_and_parse
from ..jobs import store

router = APIRouter(prefix="/analyze", tags=["analyze"])


def _process(job_id: str, zip_path: Path, work_dir: Path) -> None:
    try:
        store.update(job_id, status="running", progress="Extracting archive")
        extracted = work_dir / "extracted"
        safe_extract(zip_path, extracted)

        store.update(job_id, progress="Indexing files")
        images, annotations = index_files(extracted)

        if not images:
            raise ValueError("No images found in the archive")
        if len(images) > settings.max_images:
            raise ValueError(
                f"{len(images)} images exceeds the limit of {settings.max_images}")

        store.update(job_id, progress=f"Parsing annotations for {len(images)} images")
        ds = detect_and_parse(extracted, images, annotations)

        store.update(job_id, progress="Running checks")
        findings = run_all(ds)

        store.update(job_id, status="done", progress="Complete", result={
            "format": ds.source_format,
            "image_count": len(ds.images),
            "box_count": ds.total_boxes,
            "class_count": len(ds.class_names),
            "class_names": ds.class_names,
            "findings": [
                {
                    "check": f.check,
                    "severity": f.severity.value,
                    "title": f.title,
                    "detail": f.detail,
                    "images": f.images,
                    "count": f.count,
                }
                for f in findings
            ],
        })

    except (ExtractionError, ValueError) as e:
        store.update(job_id, status="failed", error=str(e))
    except Exception as e:
        store.update(job_id, status="failed", error=f"Unexpected error: {e}")
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


@router.post("")
async def start_analysis(background: BackgroundTasks,
                         file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(400, "Upload a .zip archive")

    work_dir = Path(tempfile.mkdtemp(prefix="labellint_"))
    zip_path = work_dir / "upload.zip"

    size = 0
    limit = settings.max_upload_mb * 1024 * 1024
    with open(zip_path, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                shutil.rmtree(work_dir, ignore_errors=True)
                raise HTTPException(
                    400, f"File exceeds the {settings.max_upload_mb} MB limit")
            out.write(chunk)

    job = store.create()
    background.add_task(_process, job.id, zip_path, work_dir)
    return {"job_id": job.id}


@router.get("/{job_id}")
def get_status(job_id: str):
    job = store.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found or expired")
    return {
        "status": job.status,
        "progress": job.progress,
        "result": job.result,
        "error": job.error,
    }


@router.post("/demo")
def analyze_demo(background: BackgroundTasks):
    demo = Path(__file__).parent.parent / "static" / "demo_dataset.zip"
    if not demo.exists():
        raise HTTPException(500, "Demo dataset not found")

    work = Path(tempfile.mkdtemp(prefix="labellint_demo_"))
    shutil.copy(demo, work / "upload.zip")

    job = store.create()
    background.add_task(_process, job.id, work / "upload.zip", work)
    return {"job_id": job.id}