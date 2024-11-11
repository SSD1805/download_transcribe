import click
from src.text_loader import TextLoader
from src.text_segmenter import TextSegmenter
from src.ner_processor import NERProcessor
from src.text_tokenizer import TextTokenizer
from src.text_saver import TextSaver
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceManager

class TextProcessor:
    def __init__(self):
        log_manager = LoggerManager()
        logger = log_manager.get_logger()
        perf_manager = PerformanceManager()

        self.text_loader = TextLoader(logger)
        self.text_segmenter = TextSegmenter(logger, perf_manager)
        self.ner_processor = NERProcessor(logger, perf_manager)
        self.text_tokenizer = TextTokenizer(logger, perf_manager)
        self.text_saver = TextSaver(logger, perf_manager)

    def process_text(self, text, filepath):
        if self.text_loader.load_text(text):
            sentences = self.text_segmenter.segment_sentences(text)
            entities = self.ner_processor.perform_ner(text)
            tokens = self.text_tokenizer.tokenize_text(text)
            self.text_saver.save_processed_text(sentences, entities, filepath)

@click.command()
@click.argument('text')
@click.argument('output_filepath')
def main(text, output_filepath):
    """
    CLI command to process input text and save the output to a specified file.
    """
    processor = TextProcessor()
    processor.process_text(text, output_filepath)

if __name__ == "__main__":
    main()
