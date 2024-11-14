import time
import threading
import psutil
from contextlib import contextmanager
from src.core.logger_manager import LoggerManager

class PerformanceTracker:
    def __init__(self):
        self.logger = LoggerManager().get_logger(__name__)
        self.memory_thread = None
        self._stop_monitoring = None

    @staticmethod
    def track(func):
# Decorator for tracking the execution time of a function.
        def wrapper(*args, **kwargs):
            start_time = time.time()
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
        """
        start_time = time.time()
        self.logger.info(f"Starting task '{task_name}'...")
        try:
            yield
        finally:
            end_time = time.time()
            self.logger.info(f"Task '{task_name}' completed in {end_time - start_time:.2f} seconds.")

    def monitor_memory_usage(self, interval=5):
        """
        Continuously monitor and log memory usage at specified intervals.
        """
        self._stop_monitoring = False

        def log_memory_usage():
            while not self._stop_monitoring:
                memory_info = psutil.virtual_memory()
                self.logger.info(f"Memory usage: {memory_info.percent}% used")
                time.sleep(interval)

        # Start memory monitoring in a separate thread
        self.memory_thread = threading.Thread(target=log_memory_usage, daemon=True)
        self.memory_thread.start()

    def stop_memory_monitoring(self):
        """
        Stops the memory usage monitoring.
        """
        self._stop_monitoring = True
        if self.memory_thread and self.memory_thread.is_alive():
            self.memory_thread.join()
        self.logger.info("Memory monitoring stopped.")
