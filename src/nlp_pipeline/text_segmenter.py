import nltk
from nltk.tokenize import sent_tokenize
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize logger and performance tracker
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()

class TextSegmenter:
    def __init__(self):
        pass

    @perf_tracker.track  # Decorator to measure performance of the segment_sentences method
    def segment_sentences(self, text):
        """
        Segments the input text into sentences.

        Args:
            text (str): The input text to segment.

        Returns:
            list: A list of segmented sentences.
        """
        if not text:
            logger.warning("No input text to segment. Please provide text before processing.")
            return []

        sentences = sent_tokenize(text)
        logger.info(f"Segmented text into {len(sentences)} sentences.")
        return sentences
