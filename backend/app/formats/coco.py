import json
from pathlib import Path

from .common import Box, Dataset, ImageRecord


def parse(root: Path, images: list[Path], json_path: Path) -> Dataset:
    data = json.loads(json_path.read_text())

    categories = {c["id"]: c["name"] for c in data.get("categories", [])}
    # COCO category ids are arbitrary; remap to contiguous 0-based
    cat_order = sorted(categories)
    cat_to_idx = {cid: i for i, cid in enumerate(cat_order)}
    class_names = {i: categories[cid] for cid, i in cat_to_idx.items()}

    by_id = {}
    for img in data.get("images", []):
        by_id[img["id"]] = img

    boxes_by_image: dict[int, list[Box]] = {}
    for ann in data.get("annotations", []):
        img = by_id.get(ann["image_id"])
        if not img:
            continue
        w, h = img["width"], img["height"]
        if w <= 0 or h <= 0:
            continue

        bx, by, bw, bh = ann["bbox"]
        boxes_by_image.setdefault(ann["image_id"], []).append(Box(
            class_id=cat_to_idx.get(ann["category_id"], 0),
            x=bx / w,
            y=by / h,
            w=bw / w,
            h=bh / h,
        ))

    path_by_name = {p.name: p for p in images}
    records = []
    for img_id, img in by_id.items():
        p = path_by_name.get(Path(img["file_name"]).name)
        if not p:
            continue
        records.append(ImageRecord(
            path=p,
            width=img["width"],
            height=img["height"],
            boxes=boxes_by_image.get(img_id, []),
        ))

    return Dataset(images=records, class_names=class_names, source_format="coco")


def write(ds: Dataset, out_path: Path) -> None:
    images, annotations = [], []
    ann_id = 1

    for i, rec in enumerate(ds.images, start=1):
        images.append({
            "id": i,
            "file_name": rec.name,
            "width": rec.width,
            "height": rec.height,
        })
        for b in rec.boxes:
            annotations.append({
                "id": ann_id,
                "image_id": i,
                "category_id": b.class_id + 1,   # COCO ids are 1-based by convention
                "bbox": [
                    round(b.x * rec.width, 2),
                    round(b.y * rec.height, 2),
                    round(b.w * rec.width, 2),
                    round(b.h * rec.height, 2),
                ],
                "area": round(b.w * rec.width * b.h * rec.height, 2),
                "iscrowd": 0,
            })
            ann_id += 1

    max_class = max(ds.class_names) if ds.class_names else -1
    categories = [
        {"id": i + 1, "name": ds.class_names.get(i, f"class_{i}"), "supercategory": "none"}
        for i in range(max_class + 1)
    ]

    out_path.write_text(json.dumps({
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }, indent=2))