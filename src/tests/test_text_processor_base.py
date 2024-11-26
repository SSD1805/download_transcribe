from unittest import TestCase
from unittest.mock import MagicMock
from abc import ABC


from src.app.pipelines.text_processing.text_processor_base import TextProcessorBase


class TestTextProcessor(TextProcessorBase, ABC):
    """
    A concrete implementation of TextProcessorBase for testing purposes.
    """
    def process(self, text: str, *args, **kwargs):
        """Mock implementation of the abstract process method."""
        return f"Processed text: {text}"


class TestTextProcessorBase(TestCase):
    """
    Unit tests for TextProcessorBase functionality using TestTextProcessor.
    """

    def setUp(self):
        self.mock_logger = MagicMock()
        self.mock_tracker = MagicMock()
        self.processor = TestTextProcessor(
            logger=self.mock_logger,
            tracker=self.mock_tracker
        )

    def test_validate_text_success(self):
        """Test successful validation of valid text."""
        valid_text = "This is a valid text."
        result = self.processor.validate_text(valid_text)
        self.assertTrue(result, "Valid text should pass validation.")
        self.mock_logger.warning.assert_not_called()

    def test_validate_text_empty(self):
        """Test validation failure for empty text."""
        invalid_text = ""
        result = self.processor.validate_text(invalid_text)
        self.assertFalse(result, "Empty text should fail validation.")
        self.mock_logger.warning.assert_called_once_with("Invalid input text_processing provided.")

    def test_validate_text_invalid_type(self):
        """Test validation failure for non-string input."""
        invalid_text = 12345
        result = self.processor.validate_text(invalid_text)
        self.assertFalse(result, "Non-string input should fail validation.")
        self.mock_logger.warning.assert_called_once_with("Invalid input text_processing provided.")

    def test_process_method(self):
        """Test the concrete implementation of the abstract process method."""
        input_text = "Sample text"
        result = self.processor.process(input_text)
        self.assertEqual(result, "Processed text: Sample text", "The process method should return the expected result.")

    def test_logger_injection(self):
        """Test that the logger is injected correctly."""
        self.assertIs(self.processor.logger, self.mock_logger, "Logger should be injected via dependency injection.")

    def test_tracker_injection(self):
        """Test that the performance tracker is injected correctly."""
        self.assertIs(self.processor.tracker, self.mock_tracker, "Tracker should be injected via dependency injection.")
