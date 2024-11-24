from nltk.tokenize import word_tokenize

from src.app.pipelines.text_processing.text_processor_base import \
    TextProcessorBase


class TextTokenizer(TextProcessorBase):
    def process(self, text: str) -> list:
        """Tokenize text_processing into words."""
        if not self.validate_text(text):
            return []

        try:
            tokens = word_tokenize(text)
            self.logger.info(f"Tokenized text_processing into {len(tokens)} tokens.")
            return tokens
        except Exception as e:
            self.logger.error(f"Error during tokenization: {e}")
            raise
