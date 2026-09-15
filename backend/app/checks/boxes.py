from ..formats.common import Dataset
from . import Finding, Severity


def degenerate_boxes(ds: Dataset, min_norm_size: float = 0.001) -> list[Finding]:
    bad = [
        rec.name for rec in ds.images
        for b in rec.boxes
        if b.w < min_norm_size or b.h < min_norm_size
    ]
    if not bad:
        return []

    return [Finding(
        check="degenerate_boxes",
        severity=Severity.ERROR,
        title=f"{len(bad)} boxes with near-zero area",
        detail=(
            "Boxes this small are almost always accidental clicks during labeling. "
            "They contribute meaningless gradients during training and should be removed."
        ),
        images=sorted(set(bad))[:60],
        count=len(bad),
    )]


def out_of_bounds(ds: Dataset, tolerance: float = 0.001) -> list[Finding]:
    bad = [
        rec.name for rec in ds.images
        for b in rec.boxes
        if (b.x < -tolerance or b.y < -tolerance
            or b.x2 > 1 + tolerance or b.y2 > 1 + tolerance)
    ]
    if not bad:
        return []

    return [Finding(
        check="out_of_bounds",
        severity=Severity.ERROR,
        title=f"{len(bad)} boxes extending past the image",
        detail=(
            "Coordinates fall outside the image bounds. Usually an export bug or a "
            "mismatch between the annotation and the image it was matched to. Some "
            "training pipelines silently clip these, others error."
        ),
        images=sorted(set(bad))[:60],
        count=len(bad),
    )]


def tiny_boxes(ds: Dataset, min_area_fraction: float = 0.0001) -> list[Finding]:
    """Boxes under ~1% of a side, which most detectors cannot learn at 640px input."""
    small = [
        rec.name for rec in ds.images
        for b in rec.boxes
        if 0 < b.area < min_area_fraction
    ]
    if not small:
        return []

    return [Finding(
        check="tiny_boxes",
        severity=Severity.WARNING,
        title=f"{len(small)} very small objects",
        detail=(
            "These objects occupy a tiny fraction of the image. At a typical 640px "
            "training resolution they may be only a few pixels across, which most "
            "detectors struggle with. Consider tiling the images or training at "
            "higher resolution."
        ),
        images=sorted(set(small))[:60],
        count=len(small),
    )]


def extreme_aspect(ds: Dataset, limit: float = 20.0) -> list[Finding]:
    bad = [
        rec.name for rec in ds.images
        for b in rec.boxes
        if b.h > 0 and (b.aspect > limit or b.aspect < 1 / limit)
    ]
    if not bad:
        return []

    return [Finding(
        check="extreme_aspect",
        severity=Severity.WARNING,
        title=f"{len(bad)} boxes with extreme aspect ratios",
        detail=(
            "Very long, thin boxes. Sometimes legitimate for things like cables or "
            "seams, often a drag mistake during labeling. Worth a look."
        ),
        images=sorted(set(bad))[:60],
        count=len(bad),
    )]