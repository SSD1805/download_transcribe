import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.core.performance_tracker import PerformanceManager

nltk.download('punkt')
nltk.download('stopwords')

class TextTokenizer:
    def __init__(self, logger, perf_manager):
        self.logger = logger
        self.perf_manager = perf_manager
        self.stopwords = set(stopwords.words('english'))

    def tokenize_text(self, text):
        if not text:
            self.logger.warning("No input text to tokenize. Please load text before processing.")
            return []

        self.perf_manager.monitor_memory_usage()
        words = word_tokenize(text)
        tokens = [word for word in words if word.isalnum() and word.lower() not in self.stopwords]
        self.logger.info(f"Tokenized text into {len(tokens)} tokens after removing stopwords.")
        return tokens
