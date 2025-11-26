from typing import List
from tracer.trace_sink import TraceSink
from tracer.trace_event import TraceEvent

class TraceBus:
    """
    Observer Pattern: Tüm subscriber'lara (Sink'lere) trace olaylarını iletir.
    SOLID: Open/Closed prensibine uygundur.
    """

    def __init__(self):
        # Java: List<TraceSink> observers
        self.observers: List[TraceSink] = []

    def register(self, sink: TraceSink) -> None:
        """
        Yeni bir TraceSink (örn: Console, File, DB) ekler.
        """
        self.observers.append(sink)

    def trace(self, event: TraceEvent) -> None:
        """
        Gelen olayı tüm kayıtlı sink'lere gönderir.
        """
        for sink in self.observers:
            sink.log(event)

    def close_all(self) -> None:
        """
        Tüm sink'leri kapatır (Dosyaları kaydet, bağlantıları kes vb.)
        """
        for sink in self.observers:
            sink.close()
