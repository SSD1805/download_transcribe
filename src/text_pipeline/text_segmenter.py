import nltk
from nltk.tokenize import sent_tokenize
from src.core.performance_tracker import PerformanceManager

class TextSegmenter:
    def __init__(self, logger, perf_manager):
        self.logger = logger
        self.perf_manager = perf_manager

    def segment_sentences(self, text):
        if not text:
            self.logger.warning("No input text to segment. Please load text before processing.")
            return []

        self.perf_manager.monitor_memory_usage()
        sentences = sent_tokenize(text)
        self.logger.info(f"Segmented text into {len(sentences)} sentences.")
        return sentences
