from src.core.batch_processor import BatchProcessor
from src.core.logger_manager import LoggerManager
from src.core.memory_monitor import MemoryMonitor
from src.core.performance_tracker import PerformanceTracker

class PipelineManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = LoggerManager().get_logger()
        self.memory_monitor = MemoryMonitor(interval=config_manager.get('memory_interval', 5))
        self.performance_tracker = PerformanceTracker()
        batch_size = config_manager.get('batch_size', 5)  # Ensure consistent batch size
        self.batch_processor = BatchProcessor(batch_size=batch_size)
        self.logger.info("PipelineManager initialized with batch size and memory monitoring.")

    def process_batch(self, func, items):
        self.batch_processor.process(func, items)
