# src/app/tasks/observers/logger_observer.py
from src.app.utils.application_logger import ApplicationLogger


class LoggerObserver:
    """
    Observer class that logs task lifecycle events using ApplicationLogger.
    """

    def __init__(self, logger=None):
        """
        Initializes the LoggerObserver with a logger instance.
        :param logger: The logger instance (defaults to ApplicationLogger).
        """
        self.logger = logger or ApplicationLogger.get_logger()

    def update(self, event: str, data: dict):
        """
        Logs task lifecycle events.
        :param event: The type of event (e.g., 'task_started', 'task_completed', 'task_failed').
        :param data: Associated event data (e.g., function name, result, or error details).
        """
        if event == "task_started":
            self.logger.info("Task started", **data)
        elif event == "task_completed":
            self.logger.info("Task completed", **data)
        elif event == "task_failed":
            self.logger.error("Task failed", **data)
        else:
            self.logger.warning("Unknown event type", event=event, data=data)
