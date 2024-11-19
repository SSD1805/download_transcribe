import time
from typing import Optional
from contextlib import contextmanager
import logging
import threading
import psutil  # Assuming psutil is used for memory monitoring


# Singleton Pattern with Dependency Injection and Factory Method
class PerformanceTracker:
    """
    Singleton PerformanceTrackerService that provides methods to track performance metrics.
    Implements a factory pattern to create and configure the tracker if none exists.
    """
    _instance: Optional['PerformanceTracker'] = None

    @classmethod
    def get_instance(cls) -> 'PerformanceTracker':
        """
        Returns the singleton instance of the PerformanceTrackerService.
        If no instance exists, it creates one.

        Returns:
            PerformanceTrackerService: Configured performance tracker instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if PerformanceTracker._instance is not None:
            raise Exception("This is a singleton class. Use the get_instance() method.")

        self.logger = logging.getLogger("performance_tracker")
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.metrics = {}
        self._monitor_thread = None
        self._stop_monitoring = threading.Event()

    @contextmanager
    def track_execution(self, operation_name: str):
        """
        Context manager to track the execution time of an operation.

        Args:
            operation_name (str): The name of the operation being tracked.
        """
        start_time = time.time()
        self.logger.info(f"Started tracking: {operation_name}")
        try:
            yield
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.metrics[operation_name] = elapsed_time
            self.logger.info(f"Completed tracking: {operation_name} - Duration: {elapsed_time:.2f} seconds")

    def log_metric(self, operation_name: str, value: float) -> None:
        """
        Log a custom performance metric.

        Args:
            operation_name (str): The name of the operation.
            value (float): The value of the metric.
        """
        self.metrics[operation_name] = value
        self.logger.info(f"Metric logged: {operation_name} - Value: {value}")

    def get_metric(self, operation_name: str) -> Optional[float]:
        """
        Retrieve a tracked metric by its name.

        Args:
            operation_name (str): The name of the operation.

        Returns:
            Optional[float]: The value of the metric, or None if not found.
        """
        return self.metrics.get(operation_name)

    def configure_monitoring(self, interval: int = 5):
        """
        Configure and start monitoring memory usage at a specified interval.

        Args:
            interval (int): The interval in seconds for monitoring memory usage.
        """
        if self._monitor_thread and self._monitor_thread.is_alive():
            self.stop_monitoring()

        self._stop_monitoring.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_memory_usage, args=(interval,), daemon=True)
        self._monitor_thread.start()
        self.logger.info(f"Performance monitoring configured with interval: {interval} seconds")

    def _monitor_memory_usage(self, interval: int):
        """
        Monitors and logs memory usage at specified intervals.

        Args:
            interval (int): Interval between memory usage checks in seconds.
        """
        while not self._stop_monitoring.is_set():
            memory_info = psutil.virtual_memory()
            self.logger.info(
                f"Memory Usage: {memory_info.percent}% used, "
                f"{memory_info.used // (1024 ** 2)}MB used, "
                f"{memory_info.available // (1024 ** 2)}MB available"
            )
            time.sleep(interval)

    def stop_monitoring(self):
        """
        Stops the memory usage monitoring thread.
        """
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._stop_monitoring.set()
            self._monitor_thread.join()
            self.logger.info("Performance monitoring stopped.")


# Example usage
if __name__ == "__main__":
    tracker = PerformanceTracker.get_instance()

    # Configure and start monitoring
    tracker.configure_monitoring(interval=10)

    # Tracking an operation
    with tracker.track_execution("Example Operation"):
        time.sleep(2)  # Simulate some work

    # Log a custom metric
    tracker.log_metric("CustomMetric", 5.5)

    # Retrieve and print a tracked metric
    metric_value = tracker.get_metric("Example Operation")
    if metric_value is not None:
        print(f"Execution time for 'Example Operation': {metric_value:.2f} seconds")

    # Stop monitoring
    tracker.stop_monitoring()
