from threading import Lock
from src.utils.logger_manager import LoggerManager
from src.utils.performance_tracker import PerformanceTracker

class LoggerService:
    """
    Provides a singleton logger instance.
    """
    _instance = None
    _lock = Lock()

    @staticmethod
    def get_instance():
        if LoggerService._instance is None:
            with LoggerService._lock:
                if LoggerService._instance is None:
                    LoggerService._instance = LoggerManager().get_logger()
        return LoggerService._instance

class PerformanceTrackerService:
    """
    Provides a singleton performance tracker instance.
    """
    _instance = None
    _lock = Lock()

    @staticmethod
    def get_instance():
        if PerformanceTrackerService._instance is None:
            with PerformanceTrackerService._lock:
                if PerformanceTrackerService._instance is None:
                    PerformanceTrackerService._instance = PerformanceTracker()
        return PerformanceTrackerService._instance

# Example usage in other classes
logger = LoggerService.get_instance()
perf_tracker = PerformanceTrackerService.get_instance()
