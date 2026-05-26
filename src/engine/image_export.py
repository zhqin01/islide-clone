"""ExportImagesEngine + LongImageEngine — slide export utilities."""

import os
from typing import List, Optional

from PIL import Image

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class ExportImagesEngine(BaseEngine):

    @staticmethod
    def apply(
        context: PresentationContext,
        output_dir: str = "",
        fmt: str = "PNG",
        dpi: int = 150,
        slides: Optional[List[int]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> EngineResult:
        """Export slides as images.

        Args:
            output_dir: Directory to save images
            fmt: "PNG" or "JPG"
            dpi: Resolution
            slides: List of slide indices, or None for all slides
            width: Optional override width in pixels
            height: Optional override height in pixels
        """
        if not output_dir:
            return EngineResult(success=False, message="Output directory is required")

        try:
            os.makedirs(output_dir, exist_ok=True)

            if slides is None:
                slides = list(range(context.slide_count))

            exported = 0
            for idx in slides:
                fname = f"slide_{idx + 1:03d}.{fmt.lower()}"
                path = os.path.join(output_dir, fname)
                context.export_slide_as_image(idx, path, fmt=fmt, dpi=dpi, width=width, height=height)
                exported += 1

            return EngineResult(
                success=True,
                message=f"Exported {exported} slides to {output_dir}",
                data={"count": exported, "output_dir": output_dir}
            )
        except NotImplementedError:
            return EngineResult(
                success=False,
                message="Slide image export requires a live PowerPoint connection.\nConnect to PowerPoint for this feature."
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))


class LongImageEngine(BaseEngine):

    @staticmethod
    def apply(
        context: PresentationContext,
        output_path: str = "",
        fmt: str = "PNG",
        dpi: int = 150,
        gap: int = 10,
        slides: Optional[List[int]] = None,
    ) -> EngineResult:
        """Combine slides into a single vertical long image.

        Args:
            output_path: Full path for the output image
            fmt: "PNG" or "JPG"
            dpi: Resolution
            gap: Gap between slides in pixels
            slides: List of slide indices, or None for all slides
        """
        import tempfile

        if not output_path:
            return EngineResult(success=False, message="Output path is required")

        if context.backend_type != "com":
            return EngineResult(
                success=False,
                message="PPT long image requires a live PowerPoint connection.\nConnect to PowerPoint for this feature."
            )

        try:
            if slides is None:
                slides = list(range(context.slide_count))

            tmp_dir = tempfile.mkdtemp()
            images = []

            for idx in slides:
                tmp_path = os.path.join(tmp_dir, f"_tmp_{idx}.png")
                context.export_slide_as_image(idx, tmp_path, fmt="PNG", dpi=dpi)
                images.append(Image.open(tmp_path))

            if not images:
                return EngineResult(success=False, message="No slides to export")

            max_width = max(img.width for img in images)
            total_height = sum(img.height for img in images) + gap * (len(images) - 1)

            combined = Image.new("RGB", (max_width, total_height), (255, 255, 255))
            y = 0
            for img in images:
                x = (max_width - img.width) // 2
                combined.paste(img, (x, y))
                y += img.height + gap

            combined.save(output_path, fmt if fmt != "JPG" else "JPEG")

            # Cleanup
            for img in images:
                img.close()
            for idx in slides:
                os.remove(os.path.join(tmp_dir, f"_tmp_{idx}.png"))
            os.rmdir(tmp_dir)

            return EngineResult(
                success=True,
                message=f"Created long image: {os.path.basename(output_path)}",
                data={"output_path": output_path, "slides": len(slides)}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
