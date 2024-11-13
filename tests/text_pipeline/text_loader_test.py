import pytest
from unittest.mock import MagicMock
from src.core.logger_manager import LoggerManager
from src.text_pipeline.text_loader import TextLoader

@pytest.fixture
def text_loader():
    logger = MagicMock()
    return TextLoader(logger), logger

def test_load_text_with_valid_text(text_loader):
    text_loader, logger = text_loader
    text = "This is a sample text."
    result = text_loader.load_text(text)
    assert result is True
    assert text_loader.input_text == text
    logger.info.assert_called_with("Text loaded for processing.")

def test_load_text_with_empty_text(text_loader):
    text_loader, logger = text_loader
    text = ""
    result = text_loader.load_text(text)
    assert result is False
    assert text_loader.input_text == ""
    logger.warning.assert_called_with("Empty text provided for loading.")

# this test needs to be completed