# src/utils/performance_and_progress_tracking.py
import time
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Iterable, Optional

from dependency_injector.wiring import Provide, inject
from tqdm import tqdm

from src.infrastructure.app.app_container import AppContainer


class TrackerStrategy(ABC):
    """
    Abstract base class for different tracking strategies.
    """

    @abstractmethod
    def track(self, *args, **kwargs):
        pass


class PerformanceTracker(TrackerStrategy):
    """
    Strategy for tracking performance metrics like CPU and memory usage.
    """

    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        self.logger = logger
        self.metrics = {}

    @contextmanager
    def track_execution(self, operation_name: str):
        """
        Context manager to track the execution time of an operation.
        """
        start_time = time.time()
        self.logger.info(f"Started tracking: {operation_name}")
        try:
            yield
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.metrics[operation_name] = elapsed_time
            self.logger.info(
                f"Completed tracking: {operation_name} - Duration: {elapsed_time:.2f} seconds"
            )

    def log_metric(self, operation_name: str, value: float) -> None:
        """
        Log a custom performance metric.
        """
        self.metrics[operation_name] = value
        self.logger.info(f"Metric logged: {operation_name} - Value: {value}")

    def get_metric(self, operation_name: str) -> Optional[float]:
        """
        Retrieve a tracked metric by its name.
        """
        return self.metrics.get(operation_name)

    def track(self, operation_name: str):
        """
        Track an operation using the performance tracker.
        """
        with self.track_execution(operation_name):
            pass


class ProgressBarTracker(TrackerStrategy):
    """
    Strategy for displaying a progress bar while iterating over an iterable.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.logger],
        performance_tracker=Provide[AppContainer.performance_tracker],
    ):
        self.logger = logger
        self.performance_tracker = performance_tracker

    def wrap(self, iterable: Iterable, description: str = "Processing", **kwargs):
        """
        Wraps an iterable with a progress bar and tracks the performance.
        """
        if iterable is None:
            self.logger.warning(
                "Provided iterable is None. Returning an empty iterable."
            )
            return iter([])

        try:
            self.logger.info(f"Starting progress bar: {description}")
            # Track overall execution time
            with self.performance_tracker.track_execution(description):
                for item in tqdm(iterable, desc=description, **kwargs):
                    yield item

            self.logger.info(f"Progress bar '{description}' completed.")

        except Exception as e:
            self.logger.error(f"Error during progress bar execution: {e}")
            raise

    def track(self, iterable: Iterable, description: str = "Processing", **kwargs):
        """
        Track the progress of an iterable using the progress bar tracker.
        """
        yield from self.wrap(iterable, description, **kwargs)


# Context Class for Tracking
class TrackerContext:
    """
    Context for using different tracking strategies.
    """

    def __init__(self, strategy: TrackerStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: TrackerStrategy):
        self._strategy = strategy

    def execute_tracking(self, *args, **kwargs):
        if isinstance(self._strategy, ProgressBarTracker):
            yield from self._strategy.track(*args, **kwargs)
        else:
            self._strategy.track(*args, **kwargs)


# Example Usage
if __name__ == "__main__":
    from src.infrastructure import container

    # Wire the AppContainer dependencies to this module
    container.wire(modules=[__name__])

    # Using Performance Tracker
    performance_tracker = PerformanceTracker()
    context = TrackerContext(performance_tracker)
    context.execute_tracking("Example Performance Tracking")

    # Using Progress Bar Tracker
    progress_tracker = ProgressBarTracker()
    context.set_strategy(progress_tracker)
    for _ in context.execute_tracking(range(10), description="Example Progress Bar"):
        time.sleep(0.1)  # Simulate work for demonstration purposes
