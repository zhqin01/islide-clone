"""Data proxy classes for the backend abstraction layer.

These dataclasses serve as opaque handles that engines use to reference
PowerPoint objects without knowing whether they come from COM or python-pptx.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BoundingBox:
    """Position and size in points (1/72 inch)."""
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    @property
    def center_x(self) -> float:
        return self.left + self.width / 2

    @property
    def center_y(self) -> float:
        return self.top + self.height / 2


@dataclass
class ShapeProxy:
    """Opaque handle to a shape on a slide.

    Holds the internal reference plus cached common properties.
    """
    internal_ref: Any
    shape_type: int
    name: str
    bounds: BoundingBox
    rotation: float = 0.0
    has_text_frame: bool = False
    slide_index: int = 0


@dataclass
class SlideProxy:
    """Opaque handle to a slide."""
    internal_ref: Any
    index: int  # 1-based for COM, 0-based for PPTX
    name: str = ""


@dataclass
class TextRunLocation:
    """Identifies a specific text run for targeted font changes."""
    shape_proxy: ShapeProxy
    paragraph_index: int
    run_index: int


@dataclass
class ParagraphLocation:
    """Identifies a specific paragraph for spacing changes."""
    shape_proxy: ShapeProxy
    paragraph_index: int


@dataclass
class ColorInfo:
    """Represents a color extracted from a shape or theme."""
    hex_code: str
    source: str = ""  # e.g. "shape fill", "theme color", "text color"


@dataclass
class SlideLayoutInfo:
    """Information about a slide layout in the presentation."""
    name: str
    index: int
    used_by_slides: list[int] = field(default_factory=list)
