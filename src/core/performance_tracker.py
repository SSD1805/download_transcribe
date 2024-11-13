import time
from src.core.logger_manager import LoggerManager

# Initialize logger using LoggerManager
logger_manager = LoggerManager()
logger = logger_manager.get_logger(__name__)

class PerformanceTracker:
    def track(func):
        """
        Decorator for tracking the execution time of a function.

        Args:
            func (callable): The function to be wrapped.
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"Starting '{func.__name__}' function...")
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"'{func.__name__}' completed in {end_time - start_time:.2f} seconds.")
            return result
        return wrapper
