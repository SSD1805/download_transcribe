import pandas as pd
import json
from src.core.services import CoreServices

logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

class TextSaver:
    def __init__(self):
        pass

    @perf_tracker.track
    def save_to_csv(self, sentences, entities, filepath):
        """
        Saves processed text data to a CSV file.

        Args:
            sentences (list): List of sentences.
            entities (list): List of entities corresponding to each sentence.
            filepath (str): Path to save the processed CSV file.
        """
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
        """
        Save processed text data, including sentences, entities, and tokens, to a plain text file.

        Args:
            sentences (list): List of sentences.
            entities (list): List of entities corresponding to each sentence.
            tokens (list): List of tokens corresponding to each sentence.
            output_file (str): Path to save the processed text file.
        """
        if not isinstance(output_file, str):
            logger.error(f"Invalid output_file type: {type(output_file)}. Expected a string.")
            raise ValueError("The output_file argument must be a string representing a file path.")

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
        """
        Save processed text data to a JSON file.

        Args:
            sentences (list): List of sentences.
            entities (list): List of entities corresponding to each sentence.
            tokens (list): List of tokens corresponding to each sentence.
            filepath (str): Path to save the JSON file.
        """
        if not isinstance(filepath, str):
            logger.error(f"Invalid filepath type: {type(filepath)}. Expected a string.")
            raise ValueError("The filepath argument must be a string representing a file path.")

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

    def save_to_jsonb(self, sentences, entities, tokens):
        """
        Returns processed text data in a JSON-B compatible format.

        Args:
            sentences (list): List of sentences.
            entities (list): List of entities corresponding to each sentence.
            tokens (list): List of tokens corresponding to each sentence.

        Returns:
            dict: Data in JSON-B compatible format.
        """
        try:
            data = [{"Sentence": sentence, "Entities": entity, "Tokens": token}
                    for sentence, entity, token in zip(sentences, entities, tokens)]
            logger.info("Processed text converted to JSON-B format.")
            return data
        except Exception as e:
            logger.error(f"Error converting processed text to JSON-B format: {e}")
            raise
