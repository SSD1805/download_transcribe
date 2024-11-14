from src.core.logger_manager import LoggerManager

class TextLoader:
    def __init__(self, logger):
        self.logger = logger
        self.input_text = ""

    def load_text(self, text):
        if not text:
            self.logger.warning("Empty text provided for loading.")
            return False
        self.input_text = text
        self.logger.info("Text loaded for processing.")
        return True
