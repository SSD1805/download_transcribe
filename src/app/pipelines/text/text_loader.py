from src.app.pipelines.text.text_processor_base import TextProcessorBase


class TextLoader(TextProcessorBase):
    def process(self, text: str) -> bool:
        """Load text for processing."""
        if not self.validate_text(text):
            return False

        self.logger.info("Text loaded for processing.")
        self.text = text
        return True
