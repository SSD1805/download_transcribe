from threading import Lock
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

class SingletonLogger:
    _instance = None
    _lock = Lock()

    @staticmethod
    def get_instance():
        if SingletonLogger._instance is None:
            with SingletonLogger._lock:
                if SingletonLogger._instance is None:
                    SingletonLogger._instance = StructLogger.get_logger()
        return SingletonLogger._instance


class SingletonPerformanceTracker:
    _instance = None
    _lock = Lock()

    @staticmethod
    def get_instance():
        if SingletonPerformanceTracker._instance is None:
            with SingletonPerformanceTracker._lock:
                if SingletonPerformanceTracker._instance is None:
                    SingletonPerformanceTracker._instance = PerformanceTracker.get_instance()
        return SingletonPerformanceTracker._instance

# Usage
logger = SingletonLogger.get_instance()
perf_tracker = SingletonPerformanceTracker.get_instance()
