"""SwapPositionsEngine — swap the positions of two selected shapes."""

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class SwapPositionsEngine(BaseEngine):

    @staticmethod
    def apply(context: PresentationContext) -> EngineResult:
        """Swap the positions of two selected shapes."""
        shapes = context.get_selected_shape_proxies()
        if len(shapes) != 2:
            return EngineResult(success=False, message="Select exactly 2 shapes to swap positions")

        try:
            a, b = shapes[0], shapes[1]
            a_left, a_top = a.bounds.left, a.bounds.top
            b_left, b_top = b.bounds.left, b.bounds.top

            context.set_shape_position(a, b_left, b_top)
            context.set_shape_position(b, a_left, a_top)

            return EngineResult(
                success=True,
                message=f"Swapped positions of '{a.name}' and '{b.name}'"
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
