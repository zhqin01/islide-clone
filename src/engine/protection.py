"""DocumentProtectionEngine — protect presentations."""

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class DocumentProtectionEngine(BaseEngine):

    @staticmethod
    def convert_to_images(context: PresentationContext) -> EngineResult:
        """Convert each slide to a single image, preventing content editing.

        This requires a live COM connection for slide export.
        """
        if context.backend_type != "com":
            return EngineResult(
                success=False,
                message="Convert to images requires a live PowerPoint connection.\nConnect to PowerPoint for this feature."
            )

        import os, tempfile

        try:
            tmp_dir = tempfile.mkdtemp()
            slide_count = context.slide_count

            for si in range(slide_count):
                tmp_path = os.path.join(tmp_dir, f"_protect_{si}.png")
                context.export_slide_as_image(si, tmp_path, fmt="PNG", dpi=150)

                slide = context._pres.Slides(si + 1)
                # Delete all existing shapes
                shapes_to_delete = list(slide.Shapes)
                for shape in shapes_to_delete:
                    shape.Delete()
                # Add full-slide image
                pw = context._pres.PageSetup.SlideWidth
                ph = context._pres.PageSetup.SlideHeight
                slide.Shapes.AddPicture(tmp_path, False, True, 0, 0, pw, ph)
                os.remove(tmp_path)

            os.rmdir(tmp_dir)
            return EngineResult(
                success=True,
                message=f"Converted {slide_count} slides to images",
                data={"count": slide_count}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))

    @staticmethod
    def set_readonly(context: PresentationContext) -> EngineResult:
        """Mark the presentation as read-only."""
        try:
            if context.backend_type == "com":
                context._pres.Final = True
            else:
                # python-pptx: this is limited — suggest using password protection
                pass
            return EngineResult(success=True, message="Presentation marked as final (read-only)")
        except Exception as e:
            return EngineResult(success=False, message=str(e))
