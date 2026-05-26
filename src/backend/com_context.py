"""PresentationContext backed by PowerPoint COM automation (pywin32).

Provides live interaction with a running PowerPoint instance.
Requires PowerPoint to be installed and running.
"""

from __future__ import annotations

import os
from typing import Any, List, Optional, Set, Tuple

import pythoncom
import win32com.client
from win32com.client import constants as pp_const

from .context import PresentationContext
from .proxies import BoundingBox, ColorInfo, ParagraphLocation, ShapeProxy, SlideProxy, TextRunLocation


class ComPresentationContext(PresentationContext):
    """COM-based context for live PowerPoint interaction."""

    def __init__(self):
        self._app = None
        self._pres = None
        self._connected = False

    # ── connection management ─────────────────────────────────

    def connect(self) -> bool:
        """Connect to the running PowerPoint application.
        Returns True if successful, False otherwise.
        """
        try:
            pythoncom.CoInitialize()
            self._app = win32com.client.Dispatch("PowerPoint.Application")
            self._app.Visible = True
            if self._app.Presentations.Count > 0:
                self._pres = self._app.ActivePresentation
            self._connected = True
            return True
        except Exception:
            return False

    def connect_to_file(self, filepath: str) -> bool:
        """Open a specific file in PowerPoint."""
        try:
            pythoncom.CoInitialize()
            self._app = win32com.client.Dispatch("PowerPoint.Application")
            self._app.Visible = True
            abs_path = os.path.abspath(filepath)
            self._pres = self._app.Presentations.Open(abs_path)
            self._filepath = abs_path
            self._connected = True
            return True
        except Exception:
            return False

    @property
    def is_connected(self) -> bool:
        return self._connected and self._pres is not None

    # ── metadata ──────────────────────────────────────────────

    @property
    def name(self) -> str:
        if self._pres:
            return os.path.splitext(os.path.basename(self._pres.Name))[0]
        return "Untitled"

    @property
    def filepath(self) -> Optional[str]:
        if self._pres:
            try:
                return self._pres.FullName
            except Exception:
                pass
        return None

    @property
    def slide_count(self) -> int:
        return self._pres.Slides.Count if self._pres else 0

    @property
    def backend_type(self) -> str:
        return "com"

    # ── selection ─────────────────────────────────────────────

    def get_selected_shape_proxies(self) -> List[ShapeProxy]:
        if not self._pres:
            return []
        try:
            sel = self._app.ActiveWindow.Selection
            if sel.Type == pp_const.ppSelectionShapes:
                slide_idx = self._app.ActiveWindow.Selection.SlideRange.SlideIndex
                result = []
                for shape in sel.ShapeRange:
                    result.append(self._com_shape_to_proxy(shape, slide_idx - 1))
                return result
        except Exception:
            pass
        return []

    def get_selected_slide_indices(self) -> List[int]:
        if not self._pres:
            return []
        try:
            sel = self._app.ActiveWindow.Selection
            if sel.Type == pp_const.ppSelectionSlides:
                indices = []
                for slide in sel.SlideRange:
                    indices.append(slide.SlideIndex)
                return indices  # 1-based in COM
        except Exception:
            pass
        return []

    # ── slides ────────────────────────────────────────────────

    def get_slide_proxies(self) -> List[SlideProxy]:
        result = []
        for i in range(1, self._pres.Slides.Count + 1):
            slide = self._pres.Slides(i)
            result.append(SlideProxy(internal_ref=slide, index=i, name=slide.Name))
        return result

    def get_all_shapes_on_slide(self, slide_index: int) -> List[ShapeProxy]:
        slide = self._pres.Slides(slide_index + 1)  # convert 0-based to 1-based
        result = []
        for shape in slide.Shapes:
            result.append(self._com_shape_to_proxy(shape, slide_index))
        return result

    def get_all_shapes_all_slides(self) -> List[Tuple[int, ShapeProxy]]:
        result = []
        for si in range(self._pres.Slides.Count):
            slide = self._pres.Slides(si + 1)
            for shape in slide.Shapes:
                result.append((si, self._com_shape_to_proxy(shape, si)))
        return result

    # ── shape geometry ────────────────────────────────────────

    def set_shape_position(self, shape_proxy: ShapeProxy, left: float, top: float) -> None:
        shape = shape_proxy.internal_ref
        shape.Left = left
        shape.Top = top
        shape_proxy.bounds.left = left
        shape_proxy.bounds.top = top

    def set_shape_size(self, shape_proxy: ShapeProxy, width: float, height: float) -> None:
        shape = shape_proxy.internal_ref
        shape.Width = width
        shape.Height = height
        shape_proxy.bounds.width = width
        shape_proxy.bounds.height = height

    def get_shape_geometry(self, shape_proxy: ShapeProxy) -> BoundingBox:
        shape = shape_proxy.internal_ref
        bb = BoundingBox(
            left=shape.Left, top=shape.Top,
            width=shape.Width, height=shape.Height,
        )
        shape_proxy.bounds = bb
        return bb

    # ── text ──────────────────────────────────────────────────

    def get_all_text_runs_all_slides(self) -> List[TextRunLocation]:
        result = []
        for si in range(self._pres.Slides.Count):
            slide = self._pres.Slides(si + 1)
            for shape in slide.Shapes:
                sp = self._com_shape_to_proxy(shape, si)
                if sp.has_text_frame:
                    try:
                        for pi in range(1, shape.TextFrame.TextRange.Paragraphs().Count + 1):
                            para = shape.TextFrame.TextRange.Paragraphs(pi)
                            for ri in range(1, para.Runs().Count + 1):
                                result.append(TextRunLocation(sp, pi - 1, ri - 1))
                    except Exception:
                        pass
        return result

    def get_text_runs_for_shapes(self, shape_proxies: List[ShapeProxy]) -> List[TextRunLocation]:
        result = []
        for sp in shape_proxies:
            if sp.has_text_frame:
                try:
                    shape = sp.internal_ref
                    for pi in range(1, shape.TextFrame.TextRange.Paragraphs().Count + 1):
                        para = shape.TextFrame.TextRange.Paragraphs(pi)
                        for ri in range(1, para.Runs().Count + 1):
                            result.append(TextRunLocation(sp, pi - 1, ri - 1))
                except Exception:
                    pass
        return result

    def set_font_for_text_run(self, location: TextRunLocation, font_name: str,
                              font_size: Optional[float] = None) -> None:
        shape = location.shape_proxy.internal_ref
        run = shape.TextFrame.TextRange.Paragraphs(location.paragraph_index + 1).Runs(location.run_index + 1)
        run.Font.Name = font_name
        if font_size is not None:
            run.Font.Size = font_size

    def set_paragraph_spacing(self, location: ParagraphLocation,
                              line_spacing: Optional[float] = None,
                              space_before: Optional[float] = None,
                              space_after: Optional[float] = None) -> None:
        shape = location.shape_proxy.internal_ref
        para = shape.TextFrame.TextRange.Paragraphs(location.paragraph_index + 1)
        if line_spacing is not None:
            para.ParagraphFormat.SpaceWithin = line_spacing
        if space_before is not None:
            para.ParagraphFormat.SpaceBefore = space_before
        if space_after is not None:
            para.ParagraphFormat.SpaceAfter = space_after

    # ── color ─────────────────────────────────────────────────

    def extract_slide_colors(self, slide_index: int) -> List[ColorInfo]:
        slide = self._pres.Slides(slide_index + 1)
        colors: List[ColorInfo] = []
        seen: Set[str] = set()
        for shape in slide.Shapes:
            try:
                if shape.Fill.ForeColor.RGB:
                    rgb = shape.Fill.ForeColor.RGB
                    hex_code = f"{rgb:06X}" if isinstance(rgb, int) else str(rgb)
                    if hex_code not in seen:
                        seen.add(hex_code)
                        colors.append(ColorInfo(hex_code=hex_code, source="shape fill"))
            except Exception:
                pass
            try:
                if shape.HasTextFrame:
                    for run in shape.TextFrame.TextRange.Runs():
                        try:
                            if run.Font.Color.RGB:
                                rgb = run.Font.Color.RGB
                                hex_code = f"{rgb:06X}" if isinstance(rgb, int) else str(rgb)
                                if hex_code not in seen:
                                    seen.add(hex_code)
                                    colors.append(ColorInfo(hex_code=hex_code, source="text color"))
                        except Exception:
                            pass
            except Exception:
                pass
        return colors

    # ── slide operations ──────────────────────────────────────

    def delete_slides(self, indices: List[int]) -> None:
        for idx in sorted(indices, reverse=True):
            self._pres.Slides(idx + 1).Delete()

    def move_slide(self, from_index: int, to_index: int) -> None:
        if from_index == to_index:
            return
        slide = self._pres.Slides(from_index + 1)
        slide.MoveTo(to_index + 1)

    def duplicate_slide(self, index: int) -> None:
        self._pres.Slides(index + 1).Duplicate()

    # ── image export ──────────────────────────────────────────

    def export_slide_as_image(self, slide_index: int, output_path: str,
                              fmt: str = "PNG", dpi: int = 150,
                              width: Optional[int] = None,
                              height: Optional[int] = None) -> None:
        abs_path = os.path.abspath(output_path)
        slide = self._pres.Slides(slide_index + 1)
        scale = dpi / 72
        w = int((width or self._pres.PageSetup.SlideWidth) * scale)
        h = int((height or self._pres.PageSetup.SlideHeight) * scale)
        filter_name = "PNG" if fmt.upper() == "PNG" else "JPG"
        slide.Export(abs_path, filter_name, w, h)

    # ── persistence ───────────────────────────────────────────

    def save(self) -> None:
        if self._pres:
            self._pres.Save()

    def save_as(self, filepath: str) -> None:
        if self._pres:
            abs_path = os.path.abspath(filepath)
            self._pres.SaveAs(abs_path)

    def close(self) -> None:
        if self._pres:
            try:
                self._pres.Close()
            except Exception:
                pass
        self._pres = None
        self._app = None
        self._connected = False

    # ── internal helpers ──────────────────────────────────────

    def _com_shape_to_proxy(self, shape, slide_index: int) -> ShapeProxy:
        try:
            has_tf = shape.HasTextFrame == -1  # True in COM
        except Exception:
            has_tf = False
        return ShapeProxy(
            internal_ref=shape,
            shape_type=shape.Type,
            name=shape.Name,
            bounds=BoundingBox(
                left=shape.Left, top=shape.Top,
                width=shape.Width, height=shape.Height,
            ),
            rotation=shape.Rotation if hasattr(shape, 'Rotation') else 0.0,
            has_text_frame=has_tf,
            slide_index=slide_index,
        )
