"""BatchCropEngine — crop multiple images to uniform size or aspect ratio."""

from typing import Optional

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class BatchCropEngine(BaseEngine):

    @staticmethod
    def apply(
        context: PresentationContext,
        target_width: Optional[float] = None,
        target_height: Optional[float] = None,
        aspect_ratio: Optional[float] = None,
    ) -> EngineResult:
        """Crop selected image shapes to uniform dimensions.

        Args:
            target_width: Target width in points (None = use largest)
            target_height: Target height in points (None = use largest)
            aspect_ratio: Target aspect ratio (width/height), overrides size args
        """
        shapes = context.get_selected_shape_proxies()
        if not shapes:
            return EngineResult(success=False, message="No shapes selected")

        try:
            if aspect_ratio is not None:
                for s in shapes:
                    current_ratio = s.bounds.width / max(s.bounds.height, 0.01)
                    if current_ratio > aspect_ratio:
                        new_w = s.bounds.height * aspect_ratio
                        context.set_shape_size(s, new_w, s.bounds.height)
                    else:
                        new_h = s.bounds.width / aspect_ratio
                        context.set_shape_size(s, s.bounds.width, new_h)
                msg = f"Cropped {len(shapes)} images to {aspect_ratio:.2f}:1 ratio"
            else:
                w = target_width or max(s.bounds.width for s in shapes)
                h = target_height or max(s.bounds.height for s in shapes)
                for s in shapes:
                    context.set_shape_size(s, w, h)
                msg = f"Cropped {len(shapes)} images to {w:.0f}x{h:.0f} pt"

            return EngineResult(success=True, message=msg, data={"count": len(shapes)})
        except Exception as e:
            return EngineResult(success=False, message=str(e))
