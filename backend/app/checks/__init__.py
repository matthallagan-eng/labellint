from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"      # will break or corrupt training
    WARNING = "warning"  # probably a mistake
    INFO = "info"        # worth knowing


@dataclass
class Finding:
    check: str
    severity: Severity
    title: str
    detail: str
    images: list[str] = field(default_factory=list)
    count: int = 0

def run_all(ds) -> list[Finding]:
    from .balance import class_balance, orphans
    from .boxes import degenerate_boxes, extreme_aspect, out_of_bounds, tiny_boxes
    from .duplicates import exact_duplicates, near_duplicates
    from .quality import blurry_images, dimension_outliers

    findings: list[Finding] = []
    for fn in (
        exact_duplicates, near_duplicates,
        blurry_images, dimension_outliers,
        degenerate_boxes, out_of_bounds, tiny_boxes, extreme_aspect,
        class_balance, orphans,
    ):
        try:
            findings.extend(fn(ds))
        except Exception as e:
            findings.append(Finding(
                check=fn.__name__,
                severity=Severity.INFO,
                title=f"Check '{fn.__name__}' could not run",
                detail=str(e),
            ))

    order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}
    return sorted(findings, key=lambda f: order[f.severity])