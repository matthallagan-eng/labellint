from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Box:
    """Normalized box. x, y are the top-left corner. All values 0-1."""
    class_id: int
    x: float
    y: float
    w: float
    h: float

    @property
    def area(self) -> float:
        return self.w * self.h

    @property
    def x2(self) -> float:
        return self.x + self.w

    @property
    def y2(self) -> float:
        return self.y + self.h

    @property
    def aspect(self) -> float:
        return self.w / self.h if self.h > 0 else float("inf")


@dataclass
class ImageRecord:
    path: Path
    width: int
    height: int
    boxes: list[Box] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.path.name


@dataclass
class Dataset:
    images: list[ImageRecord]
    class_names: dict[int, str]
    source_format: str
    orphan_labels: list[str] = field(default_factory=list)

    @property
    def total_boxes(self) -> int:
        return sum(len(i.boxes) for i in self.images)