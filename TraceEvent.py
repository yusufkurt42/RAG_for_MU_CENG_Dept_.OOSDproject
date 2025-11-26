import time
from typing import Any

class TraceEvent:
    """
    Pipeline'ın herhangi bir adımında ne olduğunu özetleyen sınıf.
    Java'daki TraceEvent sınıfının karşılığıdır.
    """

    def __init__(self, stage: str, input_data: Any, output_data: Any, duration_ms: int):
        self.stage = stage
        self.input = input_data   # Java: Object input
        self.output = output_data # Java: Object output
        self.duration_ms = duration_ms
        
        # Java: Instant.now().toEpochMilli() karşılığı:
        # Şu anki zamanı milisaniye cinsinden integer olarak saklar.
        self.timestamp = int(time.time() * 1000)

    # Python'da getter metodları (getStage vb.) yerine genellikle doğrudan
    # attribute erişimi (event.stage) kullanılır. Ancak JSON serileştirme
    # sırasında kolaylık olması için bu nesneyi sözlüğe çeviren bir metod eklemek faydalıdır.
    def to_dict(self) -> dict:
        return {
            "stage": self.stage,
            "input": self.input,
            "output": self.output,
            "timestamp": self.timestamp,
            "durationMs": self.duration_ms
        }
