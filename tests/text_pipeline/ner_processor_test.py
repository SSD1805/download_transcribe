import sys
import os
import pytest
from unittest.mock import MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from text_pipeline.ner_processor import NERProcessor

@pytest.fixture
def ner_processor():
    logger = MagicMock()
    perf_manager = MagicMock()
    return NERProcessor(logger, perf_manager), logger

def test_perform_ner_with_text(ner_processor):
    ner_processor, logger = ner_processor
    text = "Apple is looking at buying U.K. startup for $1 billion"
    expected_entities = [
        {'text': 'Apple', 'label': 'ORG', 'start': 0, 'end': 5},
        {'text': 'U.K.', 'label': 'GPE', 'start': 27, 'end': 31},
        {'text': '$1 billion', 'label': 'MONEY', 'start': 44, 'end': 54}
    ]
    ner_processor.spacy_model = MagicMock()
    ner_processor.spacy_model.return_value.ents = [
        MagicMock(text='Apple', label_='ORG', start_char=0, end_char=5),
        MagicMock(text='U.K.', label_='GPE', start_char=27, end_char=31),
        MagicMock(text='$1 billion', label_='MONEY', start_char=44, end_char=54)
    ]

    entities = ner_processor.perform_ner(text)
    assert entities == expected_entities
    logger.info.assert_called_with("Found 3 named entities.")

def test_perform_ner_with_empty_text(ner_processor):
    ner_processor, logger = ner_processor
    text = ""
    entities = ner_processor.perform_ner(text)
    assert entities == []
    logger.warning.assert_called_with("No input text for NER. Please load text before processing.")