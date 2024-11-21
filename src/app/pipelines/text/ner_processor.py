# Description: NERProcessor class to perform Named Entity Recognition (NER) on input text using spaCy.
import spacy
from src.app.utils.structlog_logger import StructLogger
from src.app.utils.tracking_utilities import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class NERProcessor:
    def __init__(self, spacy_model='en_core_web_sm'):
        try:
            self.spacy_model = spacy.load(spacy_model)
            logger.info(f"spaCy model '{spacy_model}' loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading spaCy model '{spacy_model}': {e}")
            raise

    @perf_tracker.track
    def perform_ner(self, text):
        if not text:
            logger.warning("No input text for NER. Please provide text before processing.")
            return []

        doc = self.spacy_model(text)
        entities = [{'text': ent.text, 'label': ent.label_, 'start': ent.start_char, 'end': ent.end_char} for ent in doc.ents]
        logger.info(f"Found {len(entities)} named entities.")
        return entities
