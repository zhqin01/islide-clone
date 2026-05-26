"""SlideManagerEngine — batch slide operations."""

from typing import List

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class SlideManagerEngine(BaseEngine):

    @staticmethod
    def delete(context: PresentationContext, indices: List[int]) -> EngineResult:
        if not indices:
            return EngineResult(success=False, message="No slides selected")
        try:
            context.delete_slides(indices)
            return EngineResult(success=True, message=f"Deleted {len(indices)} slides", data={"count": len(indices)})
        except Exception as e:
            return EngineResult(success=False, message=str(e))

    @staticmethod
    def duplicate(context: PresentationContext, indices: List[int]) -> EngineResult:
        if not indices:
            return EngineResult(success=False, message="No slides selected")
        try:
            for idx in sorted(indices, reverse=True):
                context.duplicate_slide(idx)
            return EngineResult(success=True, message=f"Duplicated {len(indices)} slides", data={"count": len(indices)})
        except Exception as e:
            return EngineResult(success=False, message=str(e))

    @staticmethod
    def move(context: PresentationContext, from_index: int, to_index: int) -> EngineResult:
        try:
            context.move_slide(from_index, to_index)
            return EngineResult(success=True, message=f"Moved slide {from_index + 1} to {to_index + 1}")
        except Exception as e:
            return EngineResult(success=False, message=str(e))
