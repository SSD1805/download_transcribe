# src/app/tasks/base_task.py
from abc import ABC, abstractmethod
from dependency_injector.wiring import Provide, inject
from src.infrastructure.app.app_container import AppContainer
from src.app.tasks.observers.logger_observer import LoggerObserver


class BaseTask(ABC):
    """
    Base class for tasks with centralized logging, performance tracking,
    and observer integration.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.logger],  # Use `AppContainer.logger` as the unified dependency
        tracker=Provide[AppContainer.performance_tracker],
    ):
        """
        Initialize the base task with dependency-injected logger and tracker,
        and support for observers.
        """
        self.logger = logger
        self.tracker = tracker
        self.observers = []
        # Add a default logger observer if needed
        self.add_observer(LoggerObserver(logger=self.logger))

    def add_observer(self, observer):
        """
        Adds an observer to the task.
        :param observer: An instance of an observer class implementing the `update` method.
        """
        self.observers.append(observer)

    def notify_observers(self, event: str, data: dict):
        """
        Notifies all observers of an event.
        :param event: Event type (e.g., 'task_started', 'task_completed', 'task_failed').
        :param data: Dictionary containing details of the event.
        """
        for observer in self.observers:
            observer.update(event, data)

    def execute(self, func, *args, **kwargs):
        """
        Executes a function with centralized logging, tracking, and error handling.
        :param func: The function to execute.
        """
        try:
            self.notify_observers("task_started", {"function": func.__name__})
            self.logger.info(f"Task started: {func.__name__}")
            self.tracker.track_execution_start(func.__name__, **kwargs)

            result = func(*args, **kwargs)

            self.notify_observers("task_completed", {"function": func.__name__, "result": result})
            self.logger.info(f"Task completed: {func.__name__}")
            self.tracker.track_execution_end(func.__name__, result=result)
            return result

        except Exception as e:
            error_data = {"function": func.__name__, "error": str(e)}
            self.notify_observers("task_failed", error_data)
            self.logger.error(f"Task failed: {func.__name__} with error: {e}")
            self.tracker.track_execution_error(func.__name__, error=str(e))
            raise

    @abstractmethod
    def process(self, *args, **kwargs):
        """
        Abstract method for task-specific processing.
        Subclasses must implement this method.
        """
        pass
