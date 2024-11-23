from abc import ABC, abstractmethod

from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class BaseTask(ABC):
    """
    Abstract base class for all components.
    Provides shared functionality and centralized dependency injection.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.struct_logger],
        tracker=Provide[AppContainer.performance_tracker],
    ):
        self.logger = logger
        self.tracker = tracker

    def log_event(self, message: str, level: str = "info"):
        """Log an event with the given level."""
        log_func = getattr(self.logger, level, self.logger.info)
        log_func(message)

    def track_performance(self, action: str, metadata: dict):
        """Track task performance."""
        self.tracker.track_execution(action, metadata)

    def execute(self, func, *args, **kwargs):
        """
        Execute a provided function with error handling.
        Logs events and tracks performance metrics.
        """
        self.log_event(f"Starting execution of {func.__name__}", "info")
        try:
            self.track_performance("start", {"function": func.__name__})
            result = func(*args, **kwargs)
            self.track_performance("complete", {"function": func.__name__})
            self.log_event(f"Completed execution of {func.__name__}", "info")
            return result
        except Exception as e:
            self.track_performance("error", {"function": func.__name__, "error": str(e)})
            self.log_event(f"Error in {func.__name__}: {e}", "error")
            raise

    @abstractmethod
    def process(self, *args, **kwargs):
        """Abstract method for task-specific processing."""
        pass
