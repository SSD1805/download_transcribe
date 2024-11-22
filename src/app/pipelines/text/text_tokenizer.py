from nltk.tokenize import word_tokenize

from src.app.pipelines.text.text_processor_base import TextProcessorBase


class TextTokenizer(TextProcessorBase):
    def process(self, text: str) -> list:
        """Tokenize text into words."""
        if not self.validate_text(text):
            return []

        try:
            tokens = word_tokenize(text)
            self.logger.info(f"Tokenized text into {len(tokens)} tokens.")
            return tokens
        except Exception as e:
            self.logger.error(f"Error during tokenization: {e}")
            raise
