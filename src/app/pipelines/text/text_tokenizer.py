# Description: Module to tokenize text data using NLTK library.
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.app.utils.structlog_logger import StructLogger
from src.app.utils.tracking_utilities import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class TextTokenizer:
    _stopwords = None

    @staticmethod
    def _ensure_nltk_resources():
        try:
            nltk.data.find("tokenizers/punkt")
            nltk.data.find("corpora/stopwords")
        except LookupError:
            logger.info("Downloading missing NLTK resources...")
            nltk.download("punkt")
            nltk.download("stopwords")

    @classmethod
    def get_stopwords(cls):
        if cls._stopwords is None:
            cls._ensure_nltk_resources()
            cls._stopwords = set(stopwords.words("english"))
            logger.info("Stopwords initialized successfully.")
        return cls._stopwords

    @perf_tracker.track
    def tokenize_text(self, text):
        if not text:
            logger.warning("No input text to tokenize. Please provide text before processing.")
            return []

        try:
            stopwords_set = self.get_stopwords()
            words = word_tokenize(text)
            tokens = [word for word in words if word.isalnum() and word.lower() not in stopwords_set]
            logger.info(
                f"Text tokenization complete: {len(tokens)} tokens generated from input of length {len(text)}."
            )
            return tokens
        except Exception as e:
            logger.error(f"Error during tokenization: {e}")
            raise
