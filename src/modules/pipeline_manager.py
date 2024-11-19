from src.core.batch_processor import BatchProcessor
from src.core.memory_monitor import MemoryMonitor
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

class PipelineManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.memory_monitor = MemoryMonitor(interval=config_manager.get('memory_interval', 5))
        self.performance_tracker = perf_tracker
        batch_size = config_manager.get('batch_size', 5)  # Default batch size
        self.batch_processor = BatchProcessor(batch_size=batch_size)
        logger.info("PipelineManager initialized with batch size and memory monitoring.")

    def process_batch(self, func, items):
        """
        Processes a batch of items using the provided function.

        Args:
            func (callable): Function to process each item.
            items (iterable): Items to process in batches.
        """
        self.batch_processor.process(func, items)
        logger.info("Batch processing completed.")
