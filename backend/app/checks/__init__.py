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