from src.app.pipelines.text_processing.text_processor_base import \
    TextProcessorBase


class TextLoader(TextProcessorBase):
    def process(self, text: str) -> bool:
        """Load text_processing for processing."""
        if not self.validate_text(text):
            return False

        self.logger.info("Text loaded for processing.")
        self.text = text
        return True
