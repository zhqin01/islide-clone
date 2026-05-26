"""PasteInPlaceEngine — paste copied shapes at their original positions (COM only)."""

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class PasteInPlaceEngine(BaseEngine):

    @staticmethod
    def apply(context: PresentationContext) -> EngineResult:
        """Paste the clipboard content at its original position.

        This requires a live COM connection for clipboard access.
        """
        if context.backend_type != "com":
            return EngineResult(
                success=False,
                message="Paste in Place requires a live PowerPoint connection.\nConnect to PowerPoint for this feature."
            )

        try:
            app = context._app
            app.CommandBars.ExecuteMso("PasteSourceFormatting")
            return EngineResult(success=True, message="Pasted in place")
        except Exception as e:
            return EngineResult(success=False, message=str(e))
