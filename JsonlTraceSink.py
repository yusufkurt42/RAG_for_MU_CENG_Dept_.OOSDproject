import os
import json
import datetime
from tracer.trace_sink import TraceSink
from tracer.trace_event import TraceEvent

class JsonlTraceSink(TraceSink):
    """
    Trace olaylarını JSONL formatında dosyaya yazar.
    Her satır geçerli bir JSON objesidir.
    """

    def __init__(self):
        self.file = None
        self.setup_file()

    def setup_file(self) -> None:
        try:
            # logs klasörünü oluştur
            directory = "logs"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Dosya adını oluştur (run-YYYYMMDD-HHMMSS.jsonl)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            file_name = os.path.join(directory, f"run-{timestamp}.jsonl")

            # Writer'ı başlat (append modunda, utf-8 ile)
            # buffering=1 satır satır bufferlama yapar ama biz manuel flush da kullanacağız.
            self.file = open(file_name, "a", encoding="utf-8")
            
            print(f"Trace log started: {file_name}")

        except OSError as e:
            print(f"Log dosyası oluşturulamadı: {e}")

    def log(self, event: TraceEvent) -> None:
        if self.file is None:
            return

        try:
            # Event nesnesini dict'e çeviriyoruz (TraceEvent sınıfında to_dict yazmıştık)
            event_data = event.to_dict()
            
            # JSON string'e çevir. 
            # default=str: Eğer input/output içinde serileştirilemeyen (Enum gibi) nesneler varsa
            # onları string'e çevirerek hata almayı engeller.
            json_line = json.dumps(event_data, default=str)

            # Dosyaya yaz ve satır atla
            self.file.write(json_line + "\n")
            
            # Veri kaybını önlemek için diske yazmayı zorla (Flush)
            self.file.flush()

        except IOError as e:
            print(f"Log yazma hatası: {e}")

    def close(self) -> None:
        try:
            if self.file:
                self.file.close()
        except IOError as e:
            print(f"Dosya kapatma hatası: {e}")
