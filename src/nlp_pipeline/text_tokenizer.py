import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize logger and performance tracker
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()

def download_nltk_resources():
    """
    Download necessary NLTK resources. This function should be called once
    to ensure required datasets are available.
    """
    nltk.download('punkt')
    nltk.download('stopwords')

# Call the download function to ensure resources are available
download_nltk_resources()

class TextTokenizer:
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))

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

        words = word_tokenize(text)
        tokens = [word for word in words if word.isalnum() and word.lower() not in self.stopwords]
        logger.info(f"Tokenized text into {len(tokens)} tokens after removing stopwords.")
        return tokens
