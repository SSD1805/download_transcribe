import unittest
import logging
from unittest.mock import patch
from src.utils.message_logger import MessageLogger

class TestMessageLogger(unittest.TestCase):
    @patch('src.utils.message_logger.logging')
    def test_log_message_info(self, mock_logging):
        MessageLogger.log_message("Test info message", "INFO")
        mock_logging.info.assert_called_once_with("Test info message")

    @patch('src.utils.message_logger.logging')
    def test_log_message_error(self, mock_logging):
        MessageLogger.log_message("Test error message", "ERROR")
        mock_logging.error.assert_called_once_with("Test error message")

    @patch('src.utils.message_logger.logging')
    def test_log_message_warning(self, mock_logging):
        MessageLogger.log_message("Test warning message", "WARNING")
        mock_logging.warning.assert_called_once_with("Test warning message")

    @patch('src.utils.message_logger.logging')
    def test_log_message_debug(self, mock_logging):
        MessageLogger.log_message("Test debug message", "DEBUG")
        mock_logging.debug.assert_called_once_with("Test debug message")

    @patch('src.utils.message_logger.logging')
    def test_log_message_default(self, mock_logging):
        MessageLogger.log_message("Test default message", "UNKNOWN")
        mock_logging.info.assert_called_once_with("Test default message")

if __name__ == '__main__':
    unittest.main()

#this test passed successfully