import spacy
from src.utils.logger_service import LoggerService

logger = LoggerService.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

# Initialize logger and performance tracker

class NERProcessor:
    def __init__(self, spacy_model='en_core_web_sm'):
        """
        Initializes the NERProcessor with the specified spaCy model.

        Args:
            spacy_model (str): Name of the spaCy model to load.
        """
        try:
            self.spacy_model = spacy.load(spacy_model)
            logger.info(f"spaCy model '{spacy_model}' loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading spaCy model '{spacy_model}': {e}")
            raise

    @perf_tracker.track  # Track performance of NER processing
    def perform_ner(self, text):
        """
        Performs Named Entity Recognition (NER) on the given text.

        Args:
            text (str): The input text for NER processing.

        Returns:
            list: A list of dictionaries containing entity details.
        """
        if not text:
            logger.warning("No input text for NER. Please provide text before processing.")
            return []

        doc = self.spacy_model(text)
        entities = [{'text': ent.text, 'label': ent.label_, 'start': ent.start_char, 'end': ent.end_char} for ent in doc.ents]
        logger.info(f"Found {len(entities)} named entities.")
        return entities
