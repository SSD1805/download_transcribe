import threading
import time
import traceback

import psutil

from src.infrastructure.app.app_container import AppContainer
from src.infrastructure.app.dependency_injector import Provide, inject


class MemoryMonitor:
    @inject
    def __init__(
        self,
        interval: int = 5,
        high_usage_threshold: int = 90,
        action_on_high_usage: callable = None,
        logger=Provide[AppContainer.logger],
        perf_tracker=Provide[AppContainer.performance_tracker],
    ):
        """
        Initialize the MemoryMonitor.

        Args:
            interval (int): Monitoring interval in seconds (must be > 0).
            high_usage_threshold (int): Memory usage percentage to trigger alerts (0-100).
            action_on_high_usage (callable): Callback for high memory usage events.
            logger: Logger instance for logging.
            perf_tracker: PerformanceTracker instance for tracking performance.
        """
        if interval <= 0:
            raise ValueError("Interval must be greater than 0.")
        if not (0 <= high_usage_threshold <= 100):
            raise ValueError("High usage threshold must be between 0 and 100.")

        self.interval = interval
        self.high_usage_threshold = high_usage_threshold
        self.action_on_high_usage = action_on_high_usage or self._default_high_usage_action
        self.logger = logger
        self.perf_tracker = perf_tracker
        self._stop_event = threading.Event()
        self.thread = None

    def start(self):
        """Start memory monitoring in a separate thread."""
        self.logger.info("Starting memory monitoring...")
        self._stop_event.clear()
        self.thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop memory monitoring and wait for the thread to finish."""
        self._stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=self.interval + 1)
        self.logger.info("Memory monitoring stopped.")

    def _monitor_memory(self):
        """Monitor memory usage and log statistics at regular intervals."""
        try:
            while not self._stop_event.is_set():
                with self.perf_tracker.track_execution("Memory Monitoring"):
                    memory_info = psutil.virtual_memory()
                    self.logger.info(
                        f"Memory Usage: {memory_info.percent}% used, "
                        f"{memory_info.used // (1024 ** 2)}MB used, "
                        f"{memory_info.available // (1024 ** 2)}MB available."
                    )

                    # Trigger action if memory usage exceeds threshold
                    if memory_info.percent >= self.high_usage_threshold:
                        self.logger.warning(
                            f"High memory usage detected: {memory_info.percent}%"
                        )
                        self.action_on_high_usage(memory_info)

                time.sleep(self.interval)
        except Exception as e:
            self.logger.error(f"Error during memory monitoring: {e}")
            self.logger.debug(traceback.format_exc())
        finally:
            self.logger.info("Memory monitoring thread exiting...")

    def _default_high_usage_action(self, memory_info):
        """Default action triggered on high memory usage."""
        self.logger.warning(
            f"Default action: High memory usage detected: "
            f"{memory_info.percent}% used."
        )
