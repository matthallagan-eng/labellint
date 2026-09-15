from pathlib import Path

from . import coco, voc, yolo
from .common import Box, Dataset, ImageRecord


def detect_and_parse(root: Path, images: list[Path],
                     annotations: list[Path]) -> Dataset:
    """Work out which format this dataset is in, then parse it."""
    json_files = [p for p in annotations if p.suffix.lower() == ".json"]
    xml_files = [p for p in annotations if p.suffix.lower() == ".xml"]
    txt_files = [p for p in annotations
                 if p.suffix.lower() == ".txt" and p.name not in
                 ("classes.txt", "obj.names")]

    for j in json_files:
        try:
            import json as _json
            data = _json.loads(j.read_text())
            if "images" in data and "annotations" in data:
                return coco.parse(root, images, j)
        except Exception:
            continue

    if xml_files:
        return voc.parse(root, images, xml_files)

    if txt_files:
        return yolo.parse(root, images)

    # No annotations found; still worth running image-only checks
    from PIL import Image
    records = []
    for p in images:
        try:
            with Image.open(p) as im:
                w, h = im.size
            records.append(ImageRecord(path=p, width=w, height=h))
        except Exception:
            continue
    return Dataset(images=records, class_names={}, source_format="images-only")