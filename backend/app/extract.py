import shutil
import zipfile
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
ANNOTATION_EXTS = {".txt", ".json", ".xml", ".yaml", ".yml"}


class ExtractionError(Exception):
    pass


def safe_extract(zip_path: Path, dest: Path, max_files: int = 10_000,
                 max_total_bytes: int = 2_000_000_000) -> None:
    """
    Extract a zip, refusing path traversal and zip bombs.
    """
    dest.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()

        if len(infos) > max_files:
            raise ExtractionError(f"Archive contains too many files (limit {max_files})")

        total = sum(i.file_size for i in infos)
        if total > max_total_bytes:
            raise ExtractionError("Archive expands to too much data")

        for info in infos:
            if info.is_dir():
                continue

            # Reject absolute paths and traversal
            name = Path(info.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ExtractionError(f"Unsafe path in archive: {info.filename}")

            target = (dest / name).resolve()
            if not str(target).startswith(str(dest.resolve())):
                raise ExtractionError(f"Unsafe path in archive: {info.filename}")

            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)


def index_files(root: Path) -> tuple[list[Path], list[Path]]:
    """Return (images, annotation_files) found anywhere under root."""
    images, annotations = [], []

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        # Skip macOS resource forks, which appear constantly in zips made on a Mac
        if "__MACOSX" in p.parts or p.name.startswith("._"):
            continue

        ext = p.suffix.lower()
        if ext in IMAGE_EXTS:
            images.append(p)
        elif ext in ANNOTATION_EXTS:
            annotations.append(p)

    return sorted(images), sorted(annotations)