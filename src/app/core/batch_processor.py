import traceback
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class BatchProcessor(ABC):
    @inject
    def __init__(
        self,
        batch_size: int = 10,
        use_threads: bool = False,
        timeout: int = None,
        logger=Provide[AppContainer.logger],
        perf_tracker=Provide[AppContainer.performance_tracker],
    ):
        """
        Initialize BatchProcessor.

        Args:
            batch_size (int): Number of workers/threads in the pool.
            use_threads (bool): Whether to process items using threading.
            timeout (int): Timeout for each thread (in seconds).
        """
        self.batch_size = batch_size
        self.use_threads = use_threads
        self.timeout = timeout
        self._lock = Lock()  # Thread-safe lock
        self.logger = logger
        self.perf_tracker = perf_tracker

    @abstractmethod
    def process_item(self, item):
        """
        Abstract method to process a single item.
        Must be implemented by subclasses.
        """
        pass

    def process_batch(self, items):
        """
        Process a batch of items either sequentially or using threads.

        Args:
            items (list): List of items to process.
        """
        with self.perf_tracker.track_execution("Batch Processing"):
            if self.use_threads:
                self._process_with_threads(items)
            else:
                self._process_sequentially(items)

    def _process_sequentially(self, items):
        """
        Process items sequentially.

        Args:
            items (list): List of items to process.
        """
        total_items = len(items)
        for idx, item in enumerate(items, start=1):
            try:
                with self._lock, self.perf_tracker.track_execution(f"Processing Item: {item}"):
                    self.process_item(item)
                self.logger.info(f"Item {idx}/{total_items} processed successfully: {item}")
            except Exception as e:
                self._handle_processing_exception(item, e)

    def _process_with_threads(self, items):
        """
        Process items using a thread pool.

        Args:
            items (list): List of items to process.
        """
        total_items = len(items)
        with ThreadPoolExecutor(max_workers=min(self.batch_size, total_items)) as executor:
            futures = {
                executor.submit(self._threaded_process_item, item): item
                for item in items
            }

            completed = 0
            for future in as_completed(futures, timeout=self.timeout):
                item = futures[future]
                try:
                    future.result()  # Raises exception if the task failed
                    completed += 1
                    self.logger.info(f"Item {completed}/{total_items} processed successfully: {item}")
                except Exception as e:
                    self._handle_processing_exception(item, e)

            self.logger.info(
                f"Batch processing completed: "
                f"{completed}/{total_items} items processed."
            )

    def _threaded_process_item(self, item):
        """
        Process a single item in a thread.

        Args:
            item: Item to process.
        """
        with self._lock, self.perf_tracker.track_execution(f"Threaded Processing Item: {item}"):
            self.process_item(item)

    def _handle_processing_exception(self, item, exception):
        """
        Handle exceptions that occur during item processing.

        Args:
            item: The item that failed to process.
            exception (Exception): The exception that occurred.
        """
        self.logger.error(f"Error processing item {item}: {exception}")
        self.logger.debug(traceback.format_exc())
