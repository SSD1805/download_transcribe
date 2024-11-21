# Description: Module to load text for processing.
from src.utils.structlog_logger import StructLogger
from src.utils.tracking_utilities import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class TextLoader:
    def __init__(self):
        self.input_text = ""

    @perf_tracker.track
    def load_text(self, text):
        if not text:
            logger.warning("Empty text provided for loading.")
            return False
        self.input_text = text
        logger.info("Text loaded for processing.")
        return True
