from threading import Lock
from src.infrastructure.dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer


class SingletonLogger:
    _instance = None
    _lock = Lock()

    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        self.logger = logger

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = SingletonLogger()
        return cls._instance.logger


class SingletonPerformanceTracker:
    _instance = None
    _lock = Lock()

    @inject
    def __init__(self, perf_tracker=Provide[AppContainer.performance_tracker]):
        self.perf_tracker = perf_tracker

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = SingletonPerformanceTracker()
        return cls._instance.perf_tracker


# Usage
logger = SingletonLogger.get_instance()
perf_tracker = SingletonPerformanceTracker.get_instance()
