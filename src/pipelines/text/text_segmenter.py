import nltk
from nltk.tokenize import sent_tokenize
from src.utils.logger_service import LoggerService
from src.utils.performance_tracker import PerformanceTrackerService
# Get logger and performance tracker from CoreServices
logger = LoggerService.get_logger()
perf_tracker = PerformanceTrackerService.get_performance_tracker()


class TextSegmenter:
    """
    A class to segment input text into sentences.
    """

    @staticmethod
    def ensure_nltk_resources():
        """
        Ensures necessary NLTK resources are downloaded.
        """
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            logger.info("Downloading missing NLTK resources...")
            nltk.download("punkt")

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

        try:
            # Ensure NLTK resources are available
            self.ensure_nltk_resources()

            sentences = sent_tokenize(text)
            logger.info(f"Segmented text into {len(sentences)} sentences.")
            return sentences
        except Exception as e:
            logger.error(f"Error during sentence segmentation: {e}")
            raise
