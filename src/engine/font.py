"""UniformFontEngine — replace fonts across a presentation."""

from typing import Optional

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class UniformFontEngine(BaseEngine):

    @staticmethod
    def apply(
        context: PresentationContext,
        title_font: Optional[str] = None,
        body_font: Optional[str] = None,
        target_scope: str = "all",
        title_size_threshold: float = 24.0,
    ) -> EngineResult:
        """Replace fonts throughout the presentation.

        Args:
            context: Presentation context
            title_font: Font to apply to title text (large font sizes)
            body_font: Font to apply to body text (small font sizes)
            target_scope: "all" or "selection"
            title_size_threshold: Text above this size (pt) gets the title font
        """
        if not title_font and not body_font:
            return EngineResult(success=False, message="No font specified")

        try:
            if target_scope == "selection":
                shapes = context.get_selected_shape_proxies()
                if not shapes:
                    return EngineResult(success=False, message="No shapes selected")
                runs = context.get_text_runs_for_shapes(shapes)
            else:
                runs = context.get_all_text_runs_all_slides()

            if not runs:
                return EngineResult(success=False, message="No text runs found in presentation")

            modified_title = 0
            modified_body = 0

            for loc in runs:
                try:
                    shape = loc.shape_proxy.internal_ref
                    if hasattr(shape, 'text_frame'):
                        tf = shape.text_frame
                        para = tf.paragraphs[loc.paragraph_index]
                        run = para.runs[loc.run_index]
                        current_size = run.font.size
                        if current_size is not None:
                            size_pt = current_size / 12700 if context.backend_type == "pptx" else current_size
                        else:
                            size_pt = 0
                    else:
                        size_pt = 0
                except Exception:
                    size_pt = 0

                is_title = size_pt >= title_size_threshold or size_pt == 0
                font_to_use = title_font if (is_title and title_font) else body_font

                if font_to_use:
                    context.set_font_for_text_run(loc, font_to_use)
                    if is_title:
                        modified_title += 1
                    else:
                        modified_body += 1

            msg_parts = []
            if modified_title:
                msg_parts.append(f"{modified_title} title runs")
            if modified_body:
                msg_parts.append(f"{modified_body} body runs")

            return EngineResult(
                success=True,
                message=f"Font applied: {', '.join(msg_parts)}",
                data={"title_count": modified_title, "body_count": modified_body}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
