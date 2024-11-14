import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.nlp_pipeline.text_saver import TextSaver

class TestTextSaver(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.perf_manager = MagicMock()
        self.text_saver = TextSaver(self.logger, self.perf_manager)

    @patch('src.text_processing.text_saver.pd.DataFrame.to_csv')
    def test_save_processed_text(self, mock_to_csv):
        sentences = ["This is a sentence.", "This is another sentence."]
        entities = [{"text": "sentence", "label": "NOUN"}]
        filepath = "test_output.csv"

        self.text_saver.save_processed_text(sentences, entities, filepath)

        self.perf_manager.monitor_memory_usage.assert_called_once()
        mock_to_csv.assert_called_once_with(filepath, index=False)
        self.logger.info.assert_called_with(f"Processed text saved to {filepath}.")

    def test_save_processed_text_no_sentences(self):
        sentences = []
        entities = [{"text": "sentence", "label": "NOUN"}]
        filepath = "test_output.csv"

        self.text_saver.save_processed_text(sentences, entities, filepath)

        self.logger.warning.assert_called_with("No sentences to save. Please process text before saving.")
        self.perf_manager.monitor_memory_usage.assert_not_called()

    @patch('src.text_processing.text_saver.pd.DataFrame.to_csv', side_effect=Exception("Test exception"))
    def test_save_processed_text_exception(self, mock_to_csv):
        sentences = ["This is a sentence."]
        entities = [{"text": "sentence", "label": "NOUN"}]
        filepath = "test_output.csv"

        self.text_saver.save_processed_text(sentences, entities, filepath)

        self.logger.error.assert_called_with(f"Error saving processed text to {filepath}: Test exception")

if __name__ == '__main__':
    unittest.main()

# this test needs to be completed