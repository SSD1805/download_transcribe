import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


class TextTokenizer:
    """
    Tokenizes input text into individual words, removing punctuation and stopwords.
    """
    _stopwords = None

    @staticmethod
    def _ensure_nltk_resources():
        """
        Ensure necessary NLTK resources are downloaded.
        This method is called lazily to avoid global downloads.
        """
        try:
            nltk.data.find("tokenizers/punkt")
            nltk.data.find("corpora/stopwords")
        except LookupError:
            logger.info("Downloading missing NLTK resources...")
            nltk.download("punkt")
            nltk.download("stopwords")

    @classmethod
    def get_stopwords(cls):
        """
        Lazily initializes and retrieves the English stopwords set.
        """
        if cls._stopwords is None:
            cls._ensure_nltk_resources()
            cls._stopwords = set(stopwords.words("english"))
            logger.info("Stopwords initialized successfully.")
        return cls._stopwords

    @perf_tracker.track
    def tokenize_text(self, text):
        """
        Tokenizes the input text after removing punctuation and stopwords.

        Args:
            text (str): The input text to tokenize.

        Returns:
            list: A list of filtered tokens.
        """
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
