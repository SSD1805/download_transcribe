# This module is responsible for saving the processed text to a file.
import json
import pandas as pd
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class TextSaver:
    def __init__(self):
        pass

    @perf_tracker.track
    def save_to_csv(self, sentences, entities, filepath):
        if not sentences:
            logger.warning("No sentences to save. Please process text before saving.")
            return

        try:
            processed_data = pd.DataFrame({
                'Sentence': sentences,
                'Entities': [entities for _ in range(len(sentences))]
            })
            processed_data.to_csv(filepath, index=False)
            logger.info(f"Processed text saved to CSV file at {filepath}.")
        except Exception as e:
            logger.error(f"Error saving processed text to CSV at {filepath}: {e}")
            raise

    @perf_tracker.track
    def save_to_text(self, sentences, entities, tokens, output_file: str):
        if not sentences:
            logger.warning("No sentences to save. Please process text before saving.")
            return

        try:
            with open(output_file, "a", encoding="utf-8") as f:
                for sentence, entity, token in zip(sentences, entities, tokens):
                    f.write(f"Sentence: {sentence}, Entity: {entity}, Token: {token}\n")
            logger.info(f"Processed text saved to text file at {output_file}.")
        except Exception as e:
            logger.error(f"Error saving processed text to text file at {output_file}: {e}")
            raise

    @perf_tracker.track
    def save_to_json(self, sentences, entities, tokens, filepath: str):
        if not sentences:
            logger.warning("No sentences to save. Please process text before saving.")
            return

        try:
            data = [{"Sentence": sentence, "Entities": entity, "Tokens": token}
                    for sentence, entity, token in zip(sentences, entities, tokens)]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info(f"Processed text saved to JSON file at {filepath}.")
        except Exception as e:
            logger.error(f"Error saving processed text to JSON at {filepath}: {e}")
            raise
