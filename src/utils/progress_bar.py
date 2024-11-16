from tqdm import tqdm
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

class ProgressBar:
    def __init__(self, tracker=None):
        """
        Initialize the ProgressBar.

        Args:
            tracker (PerformanceTracker, optional): Instance of PerformanceTracker for tracking performance.
        """
        self.logger = LoggerManager().get_logger()
        self.tracker = tracker or PerformanceTracker()

    def progress_bar(self, iterable, description="Processing", **kwargs):
        """
        Display a progress bar for the given iterable with performance tracking.

        Args:
            iterable (iterable): The iterable to process with a progress bar.
            description (str): A short description for the progress bar.
            **kwargs: Additional arguments to customize the tqdm progress bar.

        Returns:
            generator: A tqdm-wrapped iterable with performance tracking.
        """
        if iterable is None:
            self.logger.warning("Provided iterable is None. Returning an empty iterable.")
            return iter([])

        try:
            self.logger.info(f"Starting progress bar: {description}")

            # Track overall execution time
            with self.tracker.track_execution(description):
                for item in tqdm(iterable, desc=description, **kwargs):
                    # Track each iteration
                    with self.tracker.track_execution(f"Step in {description}"):
                        yield item

            self.logger.info(f"Progress bar '{description}' completed.")
        except Exception as e:
            self.logger.error(f"Error during progress bar execution: {e}")
            raise
