from abc import ABC, abstractmethod
from dependency_injector.wiring import Provide, inject
from src.app.tasks.observers.logger_observer import LoggerObserver
from src.infrastructure.app.app_container import AppContainer


class BaseTask(ABC):
    """
    Base class for tasks with centralized logging, performance tracking,
    and observer integration.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.logger],
        tracker=Provide[AppContainer.performance_tracker],
    ):
        self.logger = logger
        self.tracker = tracker
        self.observers = []
        self.add_observer(LoggerObserver(logger=self.logger))

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, event: str, data: dict):
        for observer in self.observers:
            observer.update(event, data)

    def execute(self, func, *args, **kwargs):
        try:
            self.notify_observers("task_started", {"function": func.__name__})
            self.logger.info(f"Task started: {func.__name__}")
            self.tracker.track_execution_start(func.__name__, **kwargs)

            result = func(*args, **kwargs)

            self.notify_observers(
                "task_completed", {"function": func.__name__, "result": result}
            )
            self.logger.info(f"Task completed: {func.__name__}")
            self.tracker.track_execution_end(func.__name__, result=result)
            return result
        except (IOError, TimeoutError) as e:
            self.handle_recoverable_error(func.__name__, e)
        except Exception as e:
            self.handle_critical_error(func.__name__, e)

    def handle_recoverable_error(self, function_name: str, error: Exception):
        self.logger.error(f"Recoverable error in {function_name}: {error}")
        self.tracker.track_execution_error(function_name, error=str(error))
        # Add retry logic or recovery mechanism if necessary.

    def handle_critical_error(self, function_name: str, error: Exception):
        self.notify_observers(
            "task_failed", {"function": function_name, "error": str(error)}
        )
        self.logger.critical(f"Critical failure in {function_name}: {error}")
        self.tracker.track_execution_error(function_name, error=str(error))
        raise

    @abstractmethod
    def process(self, *args, **kwargs):
        pass
