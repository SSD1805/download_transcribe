from nltk.tokenize import sent_tokenize

from src.app.pipelines.text.text_processor_base import TextProcessorBase


class TextSegmenter(TextProcessorBase):
    def process(self, text: str) -> list:
        """Segment text into sentences."""
        if not self.validate_text(text):
            return []

        try:
            sentences = sent_tokenize(text)
            self.logger.info(f"Segmented text into {len(sentences)} sentences.")
            return sentences
        except Exception as e:
            self.logger.error(f"Error during sentence segmentation: {e}")
            raise
