"""Base classes for engine implementations."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class EngineResult:
    """Unified result from every engine operation."""
    success: bool
    message: str = ""
    data: Any = None


class BaseEngine:
    """Marker base class. All engines are stateless."""
    pass
