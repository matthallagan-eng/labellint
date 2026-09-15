from collections import defaultdict
from hashlib import sha256

import imagehash
from PIL import Image

from ..formats.common import Dataset
from . import Finding, Severity


def exact_duplicates(ds: Dataset) -> list[Finding]:
    by_hash: dict[str, list[str]] = defaultdict(list)

    for rec in ds.images:
        try:
            digest = sha256(rec.path.read_bytes()).hexdigest()
        except Exception:
            continue
        by_hash[digest].append(rec.name)

    groups = [names for names in by_hash.values() if len(names) > 1]
    if not groups:
        return []

    total = sum(len(g) - 1 for g in groups)
    flagged = [n for g in groups for n in g[1:]]

    return [Finding(
        check="exact_duplicates",
        severity=Severity.ERROR,
        title=f"{total} duplicate images",
        detail=(
            f"Found {len(groups)} sets of byte-identical images. "
            "If duplicates land in both your train and validation splits, "
            "your validation score will be inflated and you will not know it."
        ),
        images=flagged[:60],
        count=total,
    )]


def near_duplicates(ds: Dataset, threshold: int = 5) -> list[Finding]:
    """Perceptual hashing. Threshold is max Hamming distance to call a match."""
    hashes = []
    for rec in ds.images:
        try:
            with Image.open(rec.path) as im:
                hashes.append((rec.name, imagehash.dhash(im, hash_size=8)))
        except Exception:
            continue

    seen: set[int] = set()
    pairs: list[tuple[str, str]] = []

    for i in range(len(hashes)):
        if i in seen:
            continue
        for j in range(i + 1, len(hashes)):
            if j in seen:
                continue
            if hashes[i][1] - hashes[j][1] <= threshold:
                pairs.append((hashes[i][0], hashes[j][0]))
                seen.add(j)

    if not pairs:
        return []

    return [Finding(
        check="near_duplicates",
        severity=Severity.WARNING,
        title=f"{len(pairs)} near-duplicate pairs",
        detail=(
            "Images that are visually almost identical, usually consecutive video "
            "frames. They add labeling effort without adding information, and cause "
            "the same split-leakage problem as exact duplicates."
        ),
        images=[b for _, b in pairs][:60],
        count=len(pairs),
    )]