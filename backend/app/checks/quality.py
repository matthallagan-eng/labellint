import cv2
import numpy as np

from ..formats.common import Dataset
from . import Finding, Severity


def blurry_images(ds: Dataset, absolute_threshold: float = 60.0) -> list[Finding]:
    scores: list[tuple[str, float]] = []

    for rec in ds.images:
        img = cv2.imread(str(rec.path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        scores.append((rec.name, cv2.Laplacian(img, cv2.CV_64F).var()))

    if not scores:
        return []

    values = np.array([s for _, s in scores])
    p10 = float(np.percentile(values, 10))

    # Flag anything both below the absolute floor and in the bottom decile
    flagged = [n for n, v in scores if v < absolute_threshold and v <= p10]

    if not flagged:
        return []

    return [Finding(
        check="blurry_images",
        severity=Severity.WARNING,
        title=f"{len(flagged)} possibly blurry images",
        detail=(
            "Low Laplacian variance, which usually means out of focus or motion "
            "blurred. This is a heuristic and the threshold is dataset dependent, "
            "so review before deleting. A cluster of these from one camera often "
            "means a focus problem worth fixing at the source."
        ),
        images=flagged[:60],
        count=len(flagged),
    )]


def dimension_outliers(ds: Dataset) -> list[Finding]:
    if len(ds.images) < 10:
        return []

    sizes = [(r.name, r.width * r.height) for r in ds.images]
    areas = np.array([a for _, a in sizes])
    median = float(np.median(areas))

    odd = [n for n, a in sizes if a < median * 0.25 or a > median * 4]
    if not odd:
        return []

    return [Finding(
        check="dimension_outliers",
        severity=Severity.INFO,
        title=f"{len(odd)} images with unusual dimensions",
        detail=(
            "Resolution differs sharply from the rest of the set, which often means "
            "images came from more than one source. Not a problem in itself, but "
            "worth knowing, since mixed sources can introduce domain shift."
        ),
        images=odd[:60],
        count=len(odd),
    )]