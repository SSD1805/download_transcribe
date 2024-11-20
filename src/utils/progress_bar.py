from typing import Iterable
from tqdm import tqdm
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer


class ProgressBar:
    """
    Utility for creating progress bars with optional performance tracking.
    """

    @inject
    def __init__(self, logger=Provide[AppContainer.logger], tracker=Provide[AppContainer.performance_tracker]):
        """
        Initialize the ProgressBar.

        Args:
            logger: Logger instance for logging progress.
            tracker: Performance tracker instance for tracking performance.
        """
        self.logger = logger
        self.tracker = tracker

    def wrap(self, iterable: Iterable, description: str = "Processing", **kwargs):
        """
        Wraps an iterable with a progress bar and tracks the performance.

        Args:
            iterable (Iterable): The iterable to process with a progress bar.
            description (str): A description for the progress bar.
            **kwargs: Additional arguments for customizing the tqdm progress bar.

        Yields:
            Each element of the iterable, while displaying progress.
        """
        if iterable is None:
            self.logger.warning("Provided iterable is None. Returning an empty iterable.")
            return iter([])

        try:
            self.logger.info(f"Starting progress bar: {description}")

            # Track overall execution time
            with self.tracker.track_execution(description):
                for item in tqdm(iterable, desc=description, **kwargs):
                    # Optionally, track each iteration (if needed)
                    with self.tracker.track_execution(f"Step in {description}"):
                        yield item

            self.logger.info(f"Progress bar '{description}' completed.")

        except Exception as e:
            self.logger.error(f"Error during progress bar execution: {e}")
            raise
