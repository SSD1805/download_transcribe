from src.core.batch_processor import BatchProcessor
from src.core.file_manager import FileManager
from src.core.logger_manager import LoggerManager
from src.core.memory_monitor import MemoryMonitor
from src.core.performance_tracker import PerformanceTracker


class PipelineManager:
    def __init__(self, memory_interval=5, batch_size=3):
        # Initialize core components
        self.logger_manager = LoggerManager()
        self.logger = self.logger_manager.get_logger(__name__)

        self.file_manager = FileManager()
        self.memory_monitor = MemoryMonitor(interval=memory_interval)
        self.performance_tracker = PerformanceTracker()
        self.batch_processor = BatchProcessor(batch_size=batch_size)

        self.logger.info(
            "PipelineManager initialized with memory monitoring, performance tracking, and batch processing.")

    def monitor_memory(self):
        """Starts continuous memory monitoring."""
        self.memory_monitor.monitor_usage()

    def track_performance(self, func):
        """Decorator for tracking function performance."""
        return self.performance_tracker.track(func)

    def process_batch(self, func, items):
        """Processes a batch of items with a specified function."""
        self.batch_processor.process(func, items)

    def manage_files(self, source_dir, dest_dir):
        """Manages files by moving from source to destination."""
        self.file_manager.move_files(source_dir, dest_dir)


# Example usage:
if __name__ == "__main__":
    # Initialize the PipelineManager
    pipeline = PipelineManager(memory_interval=10, batch_size=5)

    # Example task to monitor memory
    pipeline.monitor_memory()


    # Example of tracking performance of a sample function
    @pipeline.track_performance
    def sample_task():
        # Simulate task
        print("Running a sample task...")


    sample_task()

    # Example of batch processing with a simple function
    pipeline.process_batch(sample_task, ["Task1", "Task2", "Task3"])

    # Example of file management
    pipeline.manage_files("/path/to/source", "/path/to/destination")
