import xml.etree.ElementTree as ET
from pathlib import Path

from .common import Box, Dataset, ImageRecord


def parse(root: Path, images: list[Path], xml_files: list[Path]) -> Dataset:
    path_by_stem = {p.stem: p for p in images}
    class_to_id: dict[str, int] = {}
    records = []

    for xml_path in xml_files:
        try:
            tree = ET.parse(xml_path)
        except ET.ParseError:
            continue

        r = tree.getroot()
        size = r.find("size")
        if size is None:
            continue

        w = int(size.findtext("width", "0"))
        h = int(size.findtext("height", "0"))
        if w <= 0 or h <= 0:
            continue

        img_path = path_by_stem.get(xml_path.stem)
        if not img_path:
            continue

        rec = ImageRecord(path=img_path, width=w, height=h)

        for obj in r.findall("object"):
            name = obj.findtext("name", "unknown")
            if name not in class_to_id:
                class_to_id[name] = len(class_to_id)

            bb = obj.find("bndbox")
            if bb is None:
                continue

            xmin = float(bb.findtext("xmin", "0"))
            ymin = float(bb.findtext("ymin", "0"))
            xmax = float(bb.findtext("xmax", "0"))
            ymax = float(bb.findtext("ymax", "0"))

            rec.boxes.append(Box(
                class_id=class_to_id[name],
                x=xmin / w,
                y=ymin / h,
                w=(xmax - xmin) / w,
                h=(ymax - ymin) / h,
            ))

        records.append(rec)

    class_names = {v: k for k, v in class_to_id.items()}
    return Dataset(images=records, class_names=class_names, source_format="voc")


def write(ds: Dataset, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    for rec in ds.images:
        ann = ET.Element("annotation")
        ET.SubElement(ann, "filename").text = rec.name

        size = ET.SubElement(ann, "size")
        ET.SubElement(size, "width").text = str(rec.width)
        ET.SubElement(size, "height").text = str(rec.height)
        ET.SubElement(size, "depth").text = "3"

        for b in rec.boxes:
            obj = ET.SubElement(ann, "object")
            ET.SubElement(obj, "name").text = ds.class_names.get(
                b.class_id, f"class_{b.class_id}")
            ET.SubElement(obj, "difficult").text = "0"

            bb = ET.SubElement(obj, "bndbox")
            ET.SubElement(bb, "xmin").text = str(int(b.x * rec.width))
            ET.SubElement(bb, "ymin").text = str(int(b.y * rec.height))
            ET.SubElement(bb, "xmax").text = str(int(b.x2 * rec.width))
            ET.SubElement(bb, "ymax").text = str(int(b.y2 * rec.height))

        ET.ElementTree(ann).write(out_dir / f"{rec.path.stem}.xml")