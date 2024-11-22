# This module is responsible for segmenting text into sentences using NLTK's sentence tokenizer.
import nltk
from nltk.tokenize import sent_tokenize

from src.app.utils.structlog_logger import StructLogger
from src.app.utils.tracking_utilities import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class TextSegmenter:
    @staticmethod
    def ensure_nltk_resources():
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            logger.info("Downloading missing NLTK resources...")
            nltk.download("punkt")

    @perf_tracker.track
    def segment_sentences(self, text):
        if not text:
            logger.warning(
                "No input text to segment. Please provide text before processing."
            )
            return []

        try:
            self.ensure_nltk_resources()
            sentences = sent_tokenize(text)
            logger.info(f"Segmented text into {len(sentences)} sentences.")
            return sentences
        except Exception as e:
            logger.error(f"Error during sentence segmentation: {e}")
            raise
