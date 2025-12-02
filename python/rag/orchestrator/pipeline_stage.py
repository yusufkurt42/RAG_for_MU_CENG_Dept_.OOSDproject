"""Pipeline stage protocol."""

from typing import Protocol
from .context import Context


class PipelineStage(Protocol):
    """Protocol for pipeline stages."""
    
    def execute(self, context: Context) -> None:
        """Execute the stage logic."""
        ...
    
    def get_name(self) -> str:
        """Get the stage name."""
        ...
