from concurrent.futures import ThreadPoolExecutor, as_completed
from src.core.logger_manager import LoggerManager

logger_manager = LoggerManager()
logger = logger_manager.get_logger()

class BatchProcessor:
    def __init__(self, batch_size=5):
        self.batch_size = batch_size

    def process(self, func, items):
        """
        Process items in batches to improve performance.

        Args:
            func (callable): The function to process each item.
            items (list): The list of items to process.
        """
        logger.info(f"Starting batch modules with batch size: {self.batch_size}")
        with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
            futures = {executor.submit(func, item): item for item in items}
            for future in as_completed(futures):
                item = futures[future]
                try:
                    result = future.result()
                    logger.info(f"Processing complete for: {item}")
                except Exception as e:
                    logger.error(f"Error modules {item}: {e}")
        logger.info("Batch modules completed.")
