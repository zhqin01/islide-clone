"""EqualSizeEngine — make selected shapes the same size."""

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class EqualSizeEngine(BaseEngine):

    @staticmethod
    def apply(context: PresentationContext, mode: str = "both") -> EngineResult:
        """Resize selected shapes to match.

        Args:
            mode: "width", "height", or "both"
        """
        shapes = context.get_selected_shape_proxies()
        if len(shapes) < 2:
            return EngineResult(success=False, message="Select at least 2 shapes")

        try:
            if mode in ("width", "both"):
                max_w = max(s.bounds.width for s in shapes)
                for s in shapes:
                    context.set_shape_size(s, max_w, s.bounds.height)

            if mode in ("height", "both"):
                max_h = max(s.bounds.height for s in shapes)
                for s in shapes:
                    context.set_shape_size(s, s.bounds.width, max_h)

            return EngineResult(
                success=True,
                message=f"Set equal {mode} for {len(shapes)} shapes",
                data={"count": len(shapes)}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
