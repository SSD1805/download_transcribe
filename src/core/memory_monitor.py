import psutil
import time
from src.core.logger_manager import LoggerManager

class MemoryMonitor:
    def __init__(self, interval=5):
        self.interval = interval
        self._stop = False
        self.logger = LoggerManager().get_logger(__name__)

    def start(self):
        self.logger.info("Starting memory monitoring...")
        self._stop = False
        while not self._stop:
            memory_info = psutil.virtual_memory()
            self.logger.info(f"Memory Usage: {memory_info.percent}% used, {memory_info.available // (1024 ** 2)}MB available")
            time.sleep(self.interval)

    def stop(self):
        self._stop = True
        self.logger.info("Memory monitoring stopped.")
