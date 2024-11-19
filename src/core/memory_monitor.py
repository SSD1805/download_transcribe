import psutil
import time
import threading
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class MemoryMonitor:
    def __init__(self, interval=5):
        self.interval = interval
        self._stop = threading.Event()
        self.thread = None

    def start(self):
        logger.info("Starting memory monitoring...")
        self._stop.clear()
        self.thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop.set()
        if self.thread and self.thread.is_alive():
            self.thread.join()
        logger.info("Memory monitoring stopped.")

    def _monitor_memory(self):
        try:
            while not self._stop.is_set():
                memory_info = psutil.virtual_memory()
                logger.info(
                    f"Memory Usage: {memory_info.percent}% used, "
                    f"{memory_info.used // (1024 ** 2)}MB used, "
                    f"{memory_info.available // (1024 ** 2)}MB available."
                )
                time.sleep(self.interval)
        except Exception as e:
            logger.error(f"Error occurred during memory monitoring: {e}")
