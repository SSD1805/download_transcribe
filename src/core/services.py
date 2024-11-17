from threading import Lock
from src.core.services import CoreServices

# Get logger and performance tracker from CoreServices
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

class CoreServices:
    """
    Provides shared application-wide services such as logging and performance tracking.
    """
    logger = None
    perf_tracker = None
    lock = Lock()

    @staticmethod
    def get_logger():
        """
        Returns the singleton logger instance.

        Returns:
            Logger: An instance of the logger.
        """
        if CoreServices.logger is None:
            with CoreServices.lock:
                if CoreServices.logger is None:  # Double-checked locking for thread safety
                    CoreServices.logger = LoggerManager().get_logger()
        return CoreServices.logger

    @staticmethod
    def get_performance_tracker():
        """
        Returns the singleton performance tracker instance.

        Returns:
            PerformanceTracker: An instance of the performance tracker.
        """
        if CoreServices.perf_tracker is None:
            with CoreServices.lock:
                if CoreServices.perf_tracker is None:  # Double-checked locking
                    CoreServices.perf_tracker = PerformanceTracker()
        return CoreServices.perf_tracker

    @staticmethod
    def reset():
        """
        Resets the singleton services, useful for testing purposes.
        """
        with CoreServices.lock:
            CoreServices.logger = None
            CoreServices.perf_tracker = None
