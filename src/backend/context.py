"""Abstract interface for PowerPoint operations.

Defines PresentationContext — every engine writes against this ABC,
making the engine layer backend-agnostic.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

from .proxies import BoundingBox, ColorInfo, ParagraphLocation, ShapeProxy, SlideProxy, TextRunLocation


class PresentationContext(ABC):
    """Abstract interface for all PowerPoint operations.

    Two concrete implementations:
      - ComPresentationContext  (live PowerPoint via pywin32 COM)
      - PptxPresentationContext (offline .pptx file via python-pptx)
    """

    # ── metadata ──────────────────────────────────────────────

    @property
    @abstractmethod
    def name(self) -> str:
        """Presentation name (filename without path)."""
        ...

    @property
    @abstractmethod
    def filepath(self) -> Optional[str]:
        """Full path to the file, or None for unsaved COM presentations."""
        ...

    @property
    @abstractmethod
    def slide_count(self) -> int:
        """Total number of slides."""
        ...

    @property
    @abstractmethod
    def backend_type(self) -> str:
        """"com" or "pptx"."""
        ...

    # ── selection ─────────────────────────────────────────────

    @abstractmethod
    def get_selected_shape_proxies(self) -> List[ShapeProxy]:
        """Return proxies for currently-selected shapes."""
        ...

    @abstractmethod
    def get_selected_slide_indices(self) -> List[int]:
        """1-based indices of selected slides (COM) or 0-based (PPTX)."""
        ...

    # ── slides ────────────────────────────────────────────────

    @abstractmethod
    def get_slide_proxies(self) -> List[SlideProxy]:
        """Return proxies for every slide."""
        ...

    @abstractmethod
    def get_all_shapes_on_slide(self, slide_index: int) -> List[ShapeProxy]:
        """All shapes on a given slide."""
        ...

    @abstractmethod
    def get_all_shapes_all_slides(self) -> List[Tuple[int, ShapeProxy]]:
        """Flat list of (slide_index, ShapeProxy) for every shape."""
        ...

    # ── shape geometry ────────────────────────────────────────

    @abstractmethod
    def set_shape_position(self, shape_proxy: ShapeProxy, left: float, top: float) -> None:
        """Move shape to (left, top) in points."""
        ...

    @abstractmethod
    def set_shape_size(self, shape_proxy: ShapeProxy, width: float, height: float) -> None:
        """Resize shape to (width, height) in points."""
        ...

    @abstractmethod
    def get_shape_geometry(self, shape_proxy: ShapeProxy) -> BoundingBox:
        """Refresh and return the shape's current bounds."""
        ...

    # ── text ──────────────────────────────────────────────────

    @abstractmethod
    def get_all_text_runs_all_slides(self) -> List[TextRunLocation]:
        """Every text run in the presentation."""
        ...

    @abstractmethod
    def get_text_runs_for_shapes(self, shape_proxies: List[ShapeProxy]) -> List[TextRunLocation]:
        """Text runs scoped to the given shapes."""
        ...

    @abstractmethod
    def set_font_for_text_run(self, location: TextRunLocation, font_name: str,
                              font_size: Optional[float] = None) -> None:
        """Change font on a single text run."""
        ...

    @abstractmethod
    def set_paragraph_spacing(self, location: ParagraphLocation,
                              line_spacing: Optional[float] = None,
                              space_before: Optional[float] = None,
                              space_after: Optional[float] = None) -> None:
        """Adjust paragraph spacing."""
        ...

    # ── color ─────────────────────────────────────────────────

    @abstractmethod
    def extract_slide_colors(self, slide_index: int) -> List[ColorInfo]:
        """Extract color information from a slide's shapes."""
        ...

    # ── slide operations ──────────────────────────────────────

    @abstractmethod
    def delete_slides(self, indices: List[int]) -> None:
        """Delete slides by index."""
        ...

    @abstractmethod
    def move_slide(self, from_index: int, to_index: int) -> None:
        """Reorder a slide."""
        ...

    @abstractmethod
    def duplicate_slide(self, index: int) -> None:
        """Duplicate a slide."""
        ...

    # ── image export ──────────────────────────────────────────

    @abstractmethod
    def export_slide_as_image(self, slide_index: int, output_path: str,
                              fmt: str = "PNG", dpi: int = 150,
                              width: Optional[int] = None,
                              height: Optional[int] = None) -> None:
        """Export one slide to an image file."""
        ...

    # ── persistence ───────────────────────────────────────────

    @abstractmethod
    def save(self) -> None:
        """Save the presentation."""
        ...

    @abstractmethod
    def save_as(self, filepath: str) -> None:
        """Save to a new path."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Release resources."""
        ...

    # ── convenience ───────────────────────────────────────────

    def get_selected_shape_count(self) -> int:
        return len(self.get_selected_shape_proxies())

    def is_live(self) -> bool:
        return self.backend_type == "com"
