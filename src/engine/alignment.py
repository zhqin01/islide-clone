"""AlignmentEngine + DistributionEngine — align and distribute shapes."""

from typing import List

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class AlignmentEngine(BaseEngine):

    @staticmethod
    def align(context: PresentationContext, direction: str) -> EngineResult:
        """Align selected shapes to a common edge or center.

        Args:
            direction: "left", "center", "right", "top", "middle", "bottom"
        """
        shapes = context.get_selected_shape_proxies()
        if len(shapes) < 2:
            return EngineResult(success=False, message="Select at least 2 shapes to align")

        try:
            if direction in ("left", "center", "right"):
                AlignmentEngine._align_horizontal(context, shapes, direction)
            else:
                AlignmentEngine._align_vertical(context, shapes, direction)

            return EngineResult(
                success=True,
                message=f"Aligned {len(shapes)} shapes {direction}",
                data={"count": len(shapes)}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))

    @staticmethod
    def _align_horizontal(context, shapes, direction):
        if direction == "left":
            ref = min(s.bounds.left for s in shapes)
            for s in shapes:
                context.set_shape_position(s, ref, s.bounds.top)
        elif direction == "center":
            ref = sum(s.bounds.center_x for s in shapes) / len(shapes)
            for s in shapes:
                context.set_shape_position(s, ref - s.bounds.width / 2, s.bounds.top)
        elif direction == "right":
            ref = max(s.bounds.right for s in shapes)
            for s in shapes:
                context.set_shape_position(s, ref - s.bounds.width, s.bounds.top)

    @staticmethod
    def _align_vertical(context, shapes, direction):
        if direction == "top":
            ref = min(s.bounds.top for s in shapes)
            for s in shapes:
                context.set_shape_position(s, s.bounds.left, ref)
        elif direction == "middle":
            ref = sum(s.bounds.center_y for s in shapes) / len(shapes)
            for s in shapes:
                context.set_shape_position(s, s.bounds.left, ref - s.bounds.height / 2)
        elif direction == "bottom":
            ref = max(s.bounds.bottom for s in shapes)
            for s in shapes:
                context.set_shape_position(s, s.bounds.left, ref - s.bounds.height)


class DistributionEngine(BaseEngine):

    @staticmethod
    def distribute_horizontal(context: PresentationContext) -> EngineResult:
        """Distribute selected shapes evenly along the horizontal axis."""
        shapes = context.get_selected_shape_proxies()
        if len(shapes) < 3:
            return EngineResult(success=False, message="Select at least 3 shapes for distribution")

        try:
            shapes_sorted = sorted(shapes, key=lambda s: s.bounds.left)
            total_width = shapes_sorted[-1].bounds.right - shapes_sorted[0].bounds.left
            sum_widths = sum(s.bounds.width for s in shapes_sorted)
            gap = (total_width - sum_widths) / (len(shapes_sorted) - 1) if len(shapes_sorted) > 1 else 0

            x = shapes_sorted[0].bounds.left
            for s in shapes_sorted:
                context.set_shape_position(s, x, s.bounds.top)
                x += s.bounds.width + gap

            return EngineResult(
                success=True,
                message=f"Distributed {len(shapes)} shapes horizontally",
                data={"count": len(shapes), "gap": round(gap, 2)}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))

    @staticmethod
    def distribute_vertical(context: PresentationContext) -> EngineResult:
        """Distribute selected shapes evenly along the vertical axis."""
        shapes = context.get_selected_shape_proxies()
        if len(shapes) < 3:
            return EngineResult(success=False, message="Select at least 3 shapes for distribution")

        try:
            shapes_sorted = sorted(shapes, key=lambda s: s.bounds.top)
            total_height = shapes_sorted[-1].bounds.bottom - shapes_sorted[0].bounds.top
            sum_heights = sum(s.bounds.height for s in shapes_sorted)
            gap = (total_height - sum_heights) / (len(shapes_sorted) - 1) if len(shapes_sorted) > 1 else 0

            y = shapes_sorted[0].bounds.top
            for s in shapes_sorted:
                context.set_shape_position(s, s.bounds.left, y)
                y += s.bounds.height + gap

            return EngineResult(
                success=True,
                message=f"Distributed {len(shapes)} shapes vertically",
                data={"count": len(shapes), "gap": round(gap, 2)}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
