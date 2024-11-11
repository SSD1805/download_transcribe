import spacy
from src.core.performance_tracker import PerformanceManager

class NERProcessor:
    def __init__(self, logger, perf_manager, spacy_model='en_core_web_sm'):
        self.logger = logger
        self.perf_manager = perf_manager
        try:
            self.spacy_model = spacy.load(spacy_model)
            self.logger.info(f"spaCy model '{spacy_model}' loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading spaCy model '{spacy_model}': {e}")
            raise

    def perform_ner(self, text):
        if not text:
            self.logger.warning("No input text for NER. Please load text before processing.")
            return []

        self.perf_manager.monitor_memory_usage()
        doc = self.spacy_model(text)
        entities = [{'text': ent.text, 'label': ent.label_, 'start': ent.start_char, 'end': ent.end_char} for ent in doc.ents]
        self.logger.info(f"Found {len(entities)} named entities.")
        return entities
