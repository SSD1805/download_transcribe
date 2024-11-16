import time
import threading
import psutil
from contextlib import contextmanager
from src.core.logger_manager import LoggerManager


class PerformanceTracker:
    def __init__(self, monitor_interval=5):
        """
        Initialize the PerformanceTracker.

        Args:
            monitor_interval (int): Interval in seconds for logging system usage.
        """
        self.monitor_interval = monitor_interval
        self.logger = LoggerManager().get_logger()
        self.monitor_thread = None
        self._stop_monitoring = False

    @staticmethod
    def track(func):
        """
        Decorator for tracking the execution time of a function.
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger = LoggerManager().get_logger()
            logger.info(f"Starting '{func.__name__}' function...")
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"'{func.__name__}' completed in {end_time - start_time:.2f} seconds.")
            return result
        return wrapper

    @contextmanager
    def track_execution(self, task_name):
        """
        Context manager for tracking the execution time of a code block.

        Args:
            task_name (str): Name of the task to track.
        """
        start_time = time.time()
        self.logger.info(f"Starting task '{task_name}'...")
        try:
            yield
        finally:
            end_time = time.time()
            self.logger.info(f"Task '{task_name}' completed in {end_time - start_time:.2f} seconds.")

    def _log_system_usage(self):
        """
        Logs CPU, memory, network, and disk usage periodically.
        """
        while not self._stop_monitoring:
            try:
                memory_info = psutil.virtual_memory()
                cpu_percent = psutil.cpu_percent(interval=0.5)
                net_io = psutil.net_io_counters()
                disk_io = psutil.disk_io_counters()

                self.logger.info(
                    f"System Usage: CPU={cpu_percent}%, Memory={memory_info.percent}%, "
                    f"Network Sent={net_io.bytes_sent // (1024 ** 2)}MB, "
                    f"Network Received={net_io.bytes_recv // (1024 ** 2)}MB, "
                    f"Disk Read={disk_io.read_bytes // (1024 ** 2)}MB, "
                    f"Disk Write={disk_io.write_bytes // (1024 ** 2)}MB"
                )
                time.sleep(self.monitor_interval)
            except Exception as e:
                self.logger.error(f"Error while logging system usage: {e}")

    def start_monitoring(self):
        """
        Start system usage monitoring in a separate thread.
        """
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.logger.warning("Monitoring is already running.")
            return

        self._stop_monitoring = False
        self.monitor_thread = threading.Thread(target=self._log_system_usage, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Started system usage monitoring.")

    def stop_monitoring(self):
        """
        Stop system usage monitoring.
        """
        self._stop_monitoring = True
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join()
        self.logger.info("System usage monitoring stopped.")
