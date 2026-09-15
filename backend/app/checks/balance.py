from collections import Counter

from ..formats.common import Dataset
from . import Finding, Severity


def class_balance(ds: Dataset, ratio_limit: float = 20.0,
                  min_instances: int = 10) -> list[Finding]:
    counts = Counter(b.class_id for rec in ds.images for b in rec.boxes)
    if not counts:
        return []

    findings = []
    name = lambda cid: ds.class_names.get(cid, f"class_{cid}")

    rare = [cid for cid, n in counts.items() if n < min_instances]
    if rare:
        listed = ", ".join(f"{name(c)} ({counts[c]})" for c in sorted(rare))
        findings.append(Finding(
            check="rare_classes",
            severity=Severity.WARNING,
            title=f"{len(rare)} classes with very few examples",
            detail=(
                f"{listed}. Under about {min_instances} instances a class is unlikely "
                "to be learned at all. In defect detection this is usually the class "
                "you actually care about, so it is worth collecting more before training."
            ),
            count=len(rare),
        ))

    most = max(counts.values())
    least = min(counts.values())
    if least > 0 and most / least > ratio_limit:
        top = name(max(counts, key=counts.get))
        bottom = name(min(counts, key=counts.get))
        findings.append(Finding(
            check="class_imbalance",
            severity=Severity.WARNING,
            title=f"Class imbalance of {most / least:.0f} to 1",
            detail=(
                f"'{top}' has {most} instances, '{bottom}' has {least}. The model will "
                "optimize for the common class and may effectively ignore the rare one. "
                "Consider class weighting, oversampling, or collecting more data."
            ),
            count=int(most / least),
        ))

    return findings


def orphans(ds: Dataset) -> list[Finding]:
    unlabeled = [r.name for r in ds.images if not r.boxes]
    findings = []

    if unlabeled and len(unlabeled) < len(ds.images):
        findings.append(Finding(
            check="unlabeled_images",
            severity=Severity.INFO,
            title=f"{len(unlabeled)} images with no annotations",
            detail=(
                "These may be intentional negative examples, which are useful, or they "
                "may be images that were never labeled. Worth confirming which."
            ),
            images=unlabeled[:60],
            count=len(unlabeled),
        ))

    if ds.orphan_labels:
        findings.append(Finding(
            check="orphan_labels",
            severity=Severity.ERROR,
            title=f"{len(ds.orphan_labels)} annotations with no matching image",
            detail=(
                "Label files reference images that are not in the dataset. Usually "
                "means images were lost during export or the archive is incomplete."
            ),
            images=ds.orphan_labels[:60],
            count=len(ds.orphan_labels),
        ))

    return findings