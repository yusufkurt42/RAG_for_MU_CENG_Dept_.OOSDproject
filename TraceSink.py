from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tracer.trace_event import TraceEvent

class TraceSink(ABC):
    """
    Trace olaylarını kaydetmek için kullanılan arayüz.
    """

    @abstractmethod
    def log(self, event: 'TraceEvent') -> None:
        """
        Bir TraceEvent nesnesini işler (yazar/kaydeder).
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Kaynakları (dosya, bağlantı vb.) kapatır.
        """
        pass
