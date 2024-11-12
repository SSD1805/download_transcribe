import pandas as pd
from src.core.performance_tracker import PerformanceManager

class TextSaver:
    def __init__(self, logger, perf_manager):
        self.logger = logger
        self.perf_manager = perf_manager

    def save_processed_text(self, sentences, entities, filepath):
        if not sentences:
            self.logger.warning("No sentences to save. Please process text before saving.")
            return

        self.perf_manager.monitor_memory_usage()
        try:
            processed_data = pd.DataFrame({
                'Sentence': sentences,
                'Entities': [entities for _ in range(len(sentences))]
            })
            processed_data.to_csv(filepath, index=False)
            self.logger.info(f"Processed text saved to {filepath}.")
        except Exception as e:
            self.logger.error(f"Error saving processed text to {filepath}: {e}")
