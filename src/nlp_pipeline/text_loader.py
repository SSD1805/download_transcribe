from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize logger and performance tracker
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()

class TextLoader:
    def __init__(self):
        self.input_text = ""

    @perf_tracker.track  # Decorator to measure performance of load_text
    def load_text(self, text):
        """
        Loads the provided text for processing.

        Args:
            text (str): The input text to load.

        Returns:
            bool: True if text is loaded successfully, False if text is empty.
        """
        if not text:
            logger.warning("Empty text provided for loading.")
            return False
        self.input_text = text
        logger.info("Text loaded for processing.")
        return True
