from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class BatchProcessor(ABC):
    def __init__(self, batch_size=10, use_threads=False):
        self.batch_size = batch_size
        self.use_threads = use_threads

    @abstractmethod
    def process_item(self, item):
        pass

    def process_batch(self, items):
        with perf_tracker.track_execution("Batch Processing"):
            if self.use_threads:
                self._process_with_threads(items)
            else:
                self._process_sequentially(items)

    def _process_sequentially(self, items):
        for item in items:
            try:
                with perf_tracker.track_execution(f"Processing Item: {item}"):
                    self.process_item(item)
            except Exception as e:
                logger.error(f"Error processing item {item}: {e}")

    def _process_with_threads(self, items):
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
        with perf_tracker.track_execution(f"Threaded Processing Item: {item}"):
            self.process_item(item)
