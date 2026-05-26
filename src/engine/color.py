"""Color tools — extract and apply color schemes."""

from typing import List

from src.backend.context import PresentationContext
from src.backend.proxies import ColorInfo
from src.engine.base import BaseEngine, EngineResult


class ColorExtractionEngine(BaseEngine):

    @staticmethod
    def extract(context: PresentationContext) -> EngineResult:
        """Extract colors from the current or selected slide."""
        indices = context.get_selected_slide_indices()
        if indices:
            colors = context.extract_slide_colors(indices[0] - 1 if context.backend_type == "com" else indices[0])
        else:
            # Extract from first slide if nothing selected
            colors = context.extract_slide_colors(0)

        if not colors:
            return EngineResult(success=False, message="No colors found on slide")

        return EngineResult(
            success=True,
            message=f"Extracted {len(colors)} unique colors",
            data={"colors": colors}
        )


class ColorSchemeEngine(BaseEngine):

    PRESETS = {
        "Material Blue":    ["#1976D2", "#2196F3", "#64B5F6", "#BBDEFB", "#FFFFFF"],
        "Material Green":   ["#388E3C", "#4CAF50", "#81C784", "#C8E6C9", "#FFFFFF"],
        "Material Orange":  ["#F57C00", "#FF9800", "#FFB74D", "#FFE0B2", "#FFFFFF"],
        "Corporate Blue":   ["#1A237E", "#283593", "#3949AB", "#5C6BC0", "#9FA8DA"],
        "Corporate Gray":   ["#212121", "#424242", "#616161", "#9E9E9E", "#E0E0E0"],
        "Warm Red":         ["#B71C1C", "#D32F2F", "#E53935", "#EF9A9A", "#FFEBEE"],
        "Teal":             ["#004D40", "#00695C", "#00897B", "#80CBC4", "#E0F2F1"],
        "Deep Purple":      ["#311B92", "#4527A0", "#5E35B1", "#B39DDB", "#EDE7F6"],
    }

    @staticmethod
    def apply(context: PresentationContext, scheme_name: str = "Material Blue") -> EngineResult:
        """Apply a color scheme to shapes in the presentation."""
        colors = ColorSchemeEngine.PRESETS.get(scheme_name)
        if not colors:
            return EngineResult(success=False, message=f"Unknown scheme: {scheme_name}")

        try:
            applied = 0
            for si, shape_proxy in context.get_all_shapes_all_slides():
                try:
                    shape = shape_proxy.internal_ref
                    if hasattr(shape, 'fill'):
                        color_idx = applied % len(colors)
                        hex_color = colors[color_idx].lstrip('#')
                        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                        if context.backend_type == "com":
                            shape.Fill.ForeColor.RGB = (b << 16) | (g << 8) | r
                        else:
                            from pptx.util import RGBColor
                            shape.fill.solid()
                            shape.fill.fore_color.rgb = RGBColor(r, g, b)
                        applied += 1
                except Exception:
                    pass

            return EngineResult(
                success=True,
                message=f"Applied '{scheme_name}' scheme to {applied} shapes",
                data={"count": applied, "scheme": scheme_name}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
