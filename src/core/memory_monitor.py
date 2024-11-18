import psutil
import time
import threading
from src.utils.logger_service import LoggerService
from src.utils.performance_tracker import PerformanceTrackerService
# Get logger and performance tracker from CoreServices
logger = LoggerService.get_logger()
perf_tracker = PerformanceTrackerService.get_performance_tracker()

class MemoryMonitor:
    def __init__(self, interval=5, performance_tracker=None):
        """
        Initialize the MemoryMonitor.

        Args:
            interval (int): Time interval in seconds between memory usage checks.
            performance_tracker (PerformanceTracker, optional): Instance of PerformanceTracker
                to monitor the performance of memory tracking. Defaults to None.
        """
        self.interval = interval
        self._stop = threading.Event()
        self.logger = LoggerManager().get_logger()
        self.performance_tracker = performance_tracker or PerformanceTracker()
        self.thread = None

    def start(self):
        """
        Start memory monitoring in a separate thread.
        """
        self.logger.info("Starting memory monitoring...")
        self._stop.clear()
        self.thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self.thread.start()

    def stop(self):
        """
        Stop memory monitoring.
        """
        self._stop.set()
        if self.thread and self.thread.is_alive():
            self.thread.join()
        self.logger.info("Memory monitoring stopped.")

    def _monitor_memory(self):
        """
        Internal method to log memory usage periodically.
        """
        try:
            while not self._stop.is_set():
                start_time = time.time()
                memory_info = psutil.virtual_memory()
                self.logger.info(
                    f"Memory Usage: {memory_info.percent}% used, "
                    f"{memory_info.used // (1024 ** 2)}MB used, "
                    f"{memory_info.available // (1024 ** 2)}MB available"
                )
                elapsed_time = time.time() - start_time
                # Track execution time for the memory monitoring task
                self.performance_tracker.track_execution("Memory Monitoring Task", elapsed_time)
                time.sleep(self.interval)
        except Exception as e:
            self.logger.error(f"Error occurred during memory monitoring: {e}")

    def set_interval(self, interval):
        """
        Update the time interval between memory checks.

        Args:
            interval (int): New time interval in seconds.
        """
        self.interval = interval
        self.logger.info(f"Memory monitoring interval updated to {self.interval} seconds.")