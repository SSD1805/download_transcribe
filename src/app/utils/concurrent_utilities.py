# src/utils/concurrent_utilities.py
import concurrent.futures
import threading
from abc import ABC, abstractmethod


class ConcurrentTask(ABC):
    """
    Abstract base class defining a template for concurrent async_tasks.
    """

    @abstractmethod
    def task(self):
        pass

    def execute(self):
        """
        Template method to execute the task concurrently.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.task)
            return future.result()


class ExampleConcurrentTask(ConcurrentTask):
    """
    Example implementation of a concurrent task.
    """

    def task(self):
        # Simulated task
        return "Task executed!"


class ThreadManager:
    """
    Manages threading locks for thread-safe operations.
    """

    def __init__(self):
        self.lock = threading.Lock()

    def run_with_lock(self, func, *args, **kwargs):
        """
        Runs the given function with a thread lock to ensure thread safety.
        """
        with self.lock:
            return func(*args, **kwargs)
