"""AppController — session management and feature dispatch.

Owns the PresentationContext, routes feature requests to engines,
manages worker threads for long-running operations.
"""

from __future__ import annotations

import json
import os
from enum import Enum
from typing import Any, Callable, Dict, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from src.backend.context import PresentationContext
from src.backend.com_context import ComPresentationContext
from src.backend.pptx_context import PptxPresentationContext
from src.engine.base import EngineResult


class SessionMode(Enum):
    DISCONNECTED = "disconnected"
    LIVE_PPT = "live_ppt"
    PPTX_FILE = "pptx_file"


class AppController(QObject):
    """Central controller managing session lifecycle and feature dispatch."""

    session_changed = pyqtSignal(SessionMode, str)
    operation_completed = pyqtSignal(str, object)  # op_name, EngineResult
    progress_updated = pyqtSignal(int, str)         # percent, message

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._context: Optional[PresentationContext] = None
        self._mode = SessionMode.DISCONNECTED
        self._defaults: Dict[str, Any] = {}
        self._load_defaults()

    # ── session management ────────────────────────────────────

    def connect_to_powerpoint(self) -> bool:
        """Connect to running PowerPoint instance via COM."""
        ctx = ComPresentationContext()
        if ctx.connect():
            if not ctx.is_connected:
                return False
            self._context = ctx
            self._mode = SessionMode.LIVE_PPT
            self.session_changed.emit(self._mode, ctx.name)
            return True
        return False

    def open_pptx_file(self, filepath: str) -> bool:
        """Open a .pptx file in offline mode."""
        try:
            ctx = PptxPresentationContext(filepath)
            self._context = ctx
            self._mode = SessionMode.PPTX_FILE
            self.session_changed.emit(self._mode, ctx.name)
            return True
        except Exception:
            return False

    def disconnect(self) -> None:
        if self._context:
            self._context.close()
        self._context = None
        self._mode = SessionMode.DISCONNECTED
        self.session_changed.emit(self._mode, "")

    # ── properties ────────────────────────────────────────────

    @property
    def context(self) -> Optional[PresentationContext]:
        return self._context

    @property
    def mode(self) -> SessionMode:
        return self._mode

    @property
    def is_connected(self) -> bool:
        return self._context is not None

    @property
    def defaults(self) -> Dict[str, Any]:
        return self._defaults

    # ── feature dispatch ──────────────────────────────────────

    def execute_feature(self, feature_name: str, **params) -> None:
        """Dispatch a feature request to the appropriate engine."""
        if not self._context:
            self.operation_completed.emit(
                feature_name,
                EngineResult(success=False, message="No presentation open. Open a file or connect to PowerPoint first.")
            )
            return

        handler = self._map.get(feature_name)
        if handler is None:
            self.operation_completed.emit(
                feature_name,
                EngineResult(success=False, message=f"Unknown feature: {feature_name}")
            )
            return

        try:
            result = handler(self._context, **params)
            self.operation_completed.emit(feature_name, result)
        except Exception as e:
            self.operation_completed.emit(
                feature_name,
                EngineResult(success=False, message=str(e))
            )

    # ── feature handler map (lazy import to avoid circular deps) ──

    def _register_handlers(self):
        """Lazily import engines and register handlers. Called once."""
        from src.engine.font import UniformFontEngine
        from src.engine.paragraph import UniformParagraphEngine
        from src.engine.alignment import AlignmentEngine, DistributionEngine
        from src.engine.size import EqualSizeEngine
        from src.engine.layout import MatrixLayoutEngine, CircularLayoutEngine
        from src.engine.image_export import ExportImagesEngine, LongImageEngine
        from src.engine.image_crop import BatchCropEngine
        from src.engine.compress import CompressionEngine
        from src.engine.color import ColorExtractionEngine, ColorSchemeEngine
        from src.engine.slide_manager import SlideManagerEngine
        from src.engine.paste import PasteInPlaceEngine
        from src.engine.swap import SwapPositionsEngine
        from src.engine.watermark import WatermarkEngine
        from src.engine.protection import DocumentProtectionEngine
        from src.engine.tween import ShapeTweenEngine

        self._FEATURE_MAP = {
            "uniform_font":        UniformFontEngine.apply,
            "uniform_paragraph":   UniformParagraphEngine.apply,
            "align_left":          lambda ctx, **kw: AlignmentEngine.align(ctx, "left", **kw),
            "align_center":        lambda ctx, **kw: AlignmentEngine.align(ctx, "center", **kw),
            "align_right":         lambda ctx, **kw: AlignmentEngine.align(ctx, "right", **kw),
            "align_top":           lambda ctx, **kw: AlignmentEngine.align(ctx, "top", **kw),
            "align_middle":        lambda ctx, **kw: AlignmentEngine.align(ctx, "middle", **kw),
            "align_bottom":        lambda ctx, **kw: AlignmentEngine.align(ctx, "bottom", **kw),
            "distribute_h":        DistributionEngine.distribute_horizontal,
            "distribute_v":        DistributionEngine.distribute_vertical,
            "equal_width":         lambda ctx, **kw: EqualSizeEngine.apply(ctx, "width", **kw),
            "equal_height":        lambda ctx, **kw: EqualSizeEngine.apply(ctx, "height", **kw),
            "equal_both":          lambda ctx, **kw: EqualSizeEngine.apply(ctx, "both", **kw),
            "matrix_layout":       MatrixLayoutEngine.apply,
            "circular_layout":     CircularLayoutEngine.apply,
            "export_images":       ExportImagesEngine.apply,
            "export_long_image":   LongImageEngine.apply,
            "batch_crop":          BatchCropEngine.apply,
            "compress":            CompressionEngine.apply,
            "extract_colors":      ColorExtractionEngine.extract,
            "apply_color_scheme":  ColorSchemeEngine.apply,
            "slide_manager_delete":   SlideManagerEngine.delete,
            "slide_manager_duplicate": SlideManagerEngine.duplicate,
            "slide_manager_move":  SlideManagerEngine.move,
            "paste_in_place":      PasteInPlaceEngine.apply,
            "swap_positions":      SwapPositionsEngine.apply,
            "add_watermark":       WatermarkEngine.add,
            "remove_watermark":    WatermarkEngine.remove,
            "protection_convert":  DocumentProtectionEngine.convert_to_images,
            "protection_readonly": DocumentProtectionEngine.set_readonly,
            "shape_tween":         ShapeTweenEngine.apply,
        }

    _FEATURE_MAP: Dict[str, Callable] = {}
    _handlers_registered: bool = False

    def _ensure_handlers(self):
        """Lazily register handlers on first use."""
        if not self._handlers_registered:
            self._handlers_registered = True
            self._register_handlers()

    @property
    def _map(self):
        self._ensure_handlers()
        return self._FEATURE_MAP

    # ── helpers ───────────────────────────────────────────────

    def _load_defaults(self) -> None:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "resources", "config", "defaults.json"
        )
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._defaults = json.load(f)
        except Exception:
            self._defaults = {}
