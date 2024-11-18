from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.logger_service import LoggerService
from src.utils.performance_tracker import PerformanceTrackerService

# Initialize shared logger and performance tracker
logger = LoggerService.get_logger()
perf_tracker = PerformanceTrackerService.get_performance_tracker()


class BatchProcessor(ABC):
    """
    Abstract base class for batch processors with integrated performance tracking.
    """
    def __init__(self, batch_size=10, use_threads=False):
        self.batch_size = batch_size
        self.use_threads = use_threads
        self.perf_tracker = perf_tracker

    @abstractmethod
    def process_item(self, item):
        """
        Abstract method to process a single item.
        """
        pass

    def process_batch(self, items):
        """
        Process items in batches with optional threading and performance tracking.

        Args:
            items (list): The list of items to process.
        """
        with self.perf_tracker.track_execution("Batch Processing"):
            if self.use_threads:
                self._process_with_threads(items)
            else:
                self._process_sequentially(items)

    def _process_sequentially(self, items):
        """
        Process items sequentially with performance tracking for each item.
        """
        for item in items:
            try:
                with self.perf_tracker.track_execution(f"Processing Item: {item}"):
                    self.process_item(item)
            except Exception as e:
                logger.error(f"Error processing item {item}: {e}")

    def _process_with_threads(self, items):
        """
        Process items using threading for concurrency with performance tracking.
        """
        with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
            futures = {executor.submit(self._threaded_process_item, item): item for item in items}
            for future in as_completed(futures):
                item = futures[future]
                try:
                    future.result()
                    logger.info(f"Processing complete for: {item}")
                except Exception as e:
                    logger.error(f"Error processing item {item}: {e}")

    def _threaded_process_item(self, item):
        """
        Process a single item within a thread with performance tracking.
        """
        with self.perf_tracker.track_execution(f"Threaded Processing Item: {item}"):
            self.process_item(item)


class AudioBatchProcessor(BatchProcessor):
    def process_item(self, item):
        logger.info(f"Processing audio file: {item}")
        # Add specific audio processing logic here


class TextBatchProcessor(BatchProcessor):
    def process_item(self, item):
        logger.info(f"Processing text: {item}")
        # Add specific text processing logic here
