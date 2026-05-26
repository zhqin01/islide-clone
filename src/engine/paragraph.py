"""UniformParagraphEngine — set consistent paragraph spacing."""

from typing import Optional

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class UniformParagraphEngine(BaseEngine):

    @staticmethod
    def apply(
        context: PresentationContext,
        line_spacing: Optional[float] = None,
        space_before: Optional[float] = None,
        space_after: Optional[float] = None,
        target_scope: str = "all",
    ) -> EngineResult:
        """Apply uniform paragraph spacing.

        Args:
            line_spacing: Line spacing in points
            space_before: Space before paragraph in points
            space_after: Space after paragraph in points
            target_scope: "all" or "selection"
        """
        if line_spacing is None and space_before is None and space_after is None:
            return EngineResult(success=False, message="No spacing values specified")

        try:
            if target_scope == "selection":
                shapes = context.get_selected_shape_proxies()
                if not shapes:
                    return EngineResult(success=False, message="No shapes selected")
                runs = context.get_text_runs_for_shapes(shapes)
            else:
                runs = context.get_all_text_runs_all_slides()

            if not runs:
                return EngineResult(success=False, message="No text found in presentation")

            from src.backend.proxies import ParagraphLocation
            seen = set()
            modified = 0
            for loc in runs:
                key = (id(loc.shape_proxy), loc.paragraph_index)
                if key in seen:
                    continue
                seen.add(key)
                para_loc = ParagraphLocation(loc.shape_proxy, loc.paragraph_index)
                context.set_paragraph_spacing(para_loc, line_spacing, space_before, space_after)
                modified += 1

            return EngineResult(
                success=True,
                message=f"Applied paragraph spacing to {modified} paragraphs",
                data={"count": modified}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
