import spacy

from src.app.pipelines.text.text_processor_base import TextProcessorBase


class NERProcessor(TextProcessorBase):
    def __init__(self, spacy_model="en_core_web_sm", *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.spacy_model = spacy.load(spacy_model)
            self.logger.info(f"spaCy model '{spacy_model}' loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading spaCy model '{spacy_model}': {e}")
            raise

    def process(self, text: str) -> list:
        """Perform Named Entity Recognition (NER)."""
        if not self.validate_text(text):
            return []

        doc = self.spacy_model(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        self.logger.info(f"Found {len(entities)} named entities.")
        return entities
