from pathlib import Path

from PIL import Image

from .common import Box, Dataset, ImageRecord


def _read_class_names(root: Path) -> dict[int, str]:
    """Look for classes.txt, obj.names, or data.yaml."""
    for candidate in ("classes.txt", "obj.names"):
        f = next(root.rglob(candidate), None)
        if f:
            names = [l.strip() for l in f.read_text().splitlines() if l.strip()]
            return {i: n for i, n in enumerate(names)}

    yaml_file = next(root.rglob("data.yaml"), None)
    if yaml_file:
        # Minimal parse, avoids a pyyaml dependency for one field
        text = yaml_file.read_text()
        if "names:" in text:
            after = text.split("names:", 1)[1]
            raw = after.split("]")[0].strip().lstrip("[")
            names = [n.strip().strip("'\"") for n in raw.split(",") if n.strip()]
            if names:
                return {i: n for i, n in enumerate(names)}

    return {}


def parse(root: Path, images: list[Path]) -> Dataset:
    class_names = _read_class_names(root)
    records: list[ImageRecord] = []
    label_files_used: set[Path] = set()

    for img_path in images:
        try:
            with Image.open(img_path) as im:
                w, h = im.size
        except Exception:
            continue

        rec = ImageRecord(path=img_path, width=w, height=h)

        # YOLO convention: same stem, .txt, usually in a sibling "labels" dir
        candidates = [
            img_path.with_suffix(".txt"),
            img_path.parent.parent / "labels" / (img_path.stem + ".txt"),
            img_path.parent / "labels" / (img_path.stem + ".txt"),
        ]
        label_path = next((c for c in candidates if c.exists()), None)

        if label_path:
            label_files_used.add(label_path)
            for line_no, line in enumerate(label_path.read_text().splitlines(), 1):
                parts = line.split()
                if len(parts) < 5:
                    continue
                try:
                    cid = int(float(parts[0]))
                    xc, yc, bw, bh = (float(v) for v in parts[1:5])
                except ValueError:
                    continue

                rec.boxes.append(Box(
                    class_id=cid,
                    x=xc - bw / 2,
                    y=yc - bh / 2,
                    w=bw,
                    h=bh,
                ))

        records.append(rec)

    return Dataset(images=records, class_names=class_names, source_format="yolo")


def write(ds: Dataset, out_dir: Path) -> None:
    labels_dir = out_dir / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)

    for rec in ds.images:
        lines = []
        for b in rec.boxes:
            xc = b.x + b.w / 2
            yc = b.y + b.h / 2
            lines.append(f"{b.class_id} {xc:.6f} {yc:.6f} {b.w:.6f} {b.h:.6f}")
        (labels_dir / f"{rec.path.stem}.txt").write_text("\n".join(lines))

    if ds.class_names:
        ordered = [ds.class_names.get(i, f"class_{i}")
                   for i in range(max(ds.class_names) + 1)]
        (out_dir / "classes.txt").write_text("\n".join(ordered))