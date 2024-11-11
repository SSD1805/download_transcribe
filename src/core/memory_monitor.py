import psutil
import time
from src.core.logger_manager import LoggerManager

logger_manager = LoggerManager()
logger = logger_manager.get_logger(__name__)

class MemoryMonitor:
    def __init__(self, interval=5):
        self.interval = interval

    def monitor_usage(self):
        """
        Continuously monitor and log memory usage at set intervals.
        """
        logger.info("Starting memory monitoring...")
        try:
            while True:
                memory_info = psutil.virtual_memory()
                logger.info(f"Memory Usage: {memory_info.percent}% used, {memory_info.available // (1024 ** 2)}MB available")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("Memory monitoring stopped.")
        except Exception as e:
            logger.error(f"Error in memory monitoring: {e}")
