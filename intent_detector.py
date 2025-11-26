from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Type hinting için (Circular import'u önlemek adına)
if TYPE_CHECKING:
    from orchestrator.context import Context

class IntentDetector(ABC):
    
    @abstractmethod
    def execute(self, context: 'Context') -> None:
        """
        Intent tespitini gerçekleştirir ve context nesnesini günceller.
        """
        pass

    @property
    def name(self) -> str:
        """
        Bileşenin adını döndürür.
        """
        return "intent_detector"

