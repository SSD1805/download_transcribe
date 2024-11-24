import json

import pandas as pd

from src.app.pipelines.text_processing.text_processor_base import \
    TextProcessorBase


class TextSaver(TextProcessorBase):
    def save_to_csv(self, sentences, entities, filepath):
        """Save processed data to a CSV file."""
        try:
            data = pd.DataFrame({"Sentences": sentences, "Entities": entities})
            data.to_csv(filepath, index=False)
            self.logger.info(f"Data saved to CSV at {filepath}.")
        except Exception as e:
            self.logger.error(f"Error saving data to CSV: {e}")
            raise

    def save_to_json(self, data, filepath):
        """Save processed data to a JSON file."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Data saved to JSON at {filepath}.")
        except Exception as e:
            self.logger.error(f"Error saving data to JSON: {e}")
            raise
