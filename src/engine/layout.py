"""MatrixLayoutEngine + CircularLayoutEngine — arrange shapes in grids and circles."""

import math

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class MatrixLayoutEngine(BaseEngine):

    @staticmethod
    def apply(
        context: PresentationContext,
        columns: int = 3,
        h_gap: float = 20.0,
        v_gap: float = 20.0,
        start_left: float = 50.0,
        start_top: float = 50.0,
    ) -> EngineResult:
        """Arrange selected shapes in a grid.

        Args:
            columns: Number of columns
            h_gap: Horizontal gap between cells (points)
            v_gap: Vertical gap between cells (points)
            start_left: Starting X position (points)
            start_top: Starting Y position (points)
        """
        shapes = context.get_selected_shape_proxies()
        if not shapes:
            return EngineResult(success=False, message="No shapes selected")

        if columns < 1:
            return EngineResult(success=False, message="Columns must be >= 1")

        try:
            max_w = max(s.bounds.width for s in shapes)
            max_h = max(s.bounds.height for s in shapes)

            for i, shape in enumerate(shapes):
                col = i % columns
                row = i // columns
                x = start_left + col * (max_w + h_gap)
                y = start_top + row * (max_h + v_gap)
                context.set_shape_position(shape, x, y)

            rows = math.ceil(len(shapes) / columns)
            return EngineResult(
                success=True,
                message=f"Arranged {len(shapes)} shapes in {columns}x{rows} grid",
                data={"count": len(shapes), "columns": columns, "rows": rows}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))


class CircularLayoutEngine(BaseEngine):

    @staticmethod
    def apply(
        context: PresentationContext,
        radius: float = 200.0,
        start_angle: float = 0.0,
        clockwise: bool = True,
        rotate_shapes: bool = False,
    ) -> EngineResult:
        """Arrange selected shapes in a circle.

        Args:
            radius: Circle radius in points
            start_angle: Starting angle in degrees (0 = right)
            clockwise: Direction of arrangement
            rotate_shapes: Whether to rotate each shape to face the center
        """
        shapes = context.get_selected_shape_proxies()
        if not shapes:
            return EngineResult(success=False, message="No shapes selected")

        try:
            # Compute center from current positions
            cx = sum(s.bounds.center_x for s in shapes) / len(shapes)
            cy = sum(s.bounds.center_y for s in shapes) / len(shapes)

            direction = -1 if clockwise else 1
            angle_step = 360.0 / len(shapes)
            start_rad = math.radians(start_angle)

            for i, shape in enumerate(shapes):
                angle = start_rad + direction * math.radians(i * angle_step)
                x = cx + radius * math.cos(angle) - shape.bounds.width / 2
                y = cy + radius * math.sin(angle) - shape.bounds.height / 2
                context.set_shape_position(shape, x, y)

                if rotate_shapes:
                    # Set rotation so shape points toward center
                    deg = i * angle_step
                    if hasattr(shape.internal_ref, 'Rotation'):
                        shape.internal_ref.Rotation = deg

            return EngineResult(
                success=True,
                message=f"Arranged {len(shapes)} shapes in a circle",
                data={"count": len(shapes), "radius": radius}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
