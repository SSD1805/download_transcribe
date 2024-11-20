from dask.distributed import Client

from src.core.batch_processor import BatchProcessor
from src.core.memory_monitor import MemoryMonitor
from src.modules.config_manager import ConfigManager
from src.pipelines.text.ner_processor import NERProcessor
from src.pipelines.text.text_loader import TextLoader
from src.pipelines.text.text_saver import TextSaver
from src.pipelines.text.text_segmenter import TextSegmenter
from src.pipelines.text.text_tokenizer import TextTokenizer

# Get logger and performance tracker from CoreServices
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

class PipelineManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = LoggerManager().get_logger()
        self.memory_monitor = MemoryMonitor(interval=config_manager.get('memory_interval', 5))
        self.performance_tracker = PerformanceTracker()
        self.client = Client("tcp://dask_scheduler:8786")  # Connect to Dask scheduler
        self.batch_processor = BatchProcessor(batch_size=config_manager.get('batch_size', 5))

    def process_batch(self, text_batch, output_file):
        """
        Process a batch of texts, including loading, segmenting, tokenizing, NER, and saving results.
        """
        results = []

        # Process each item in the batch
        for text in text_batch:
            try:
                with self.performance_tracker.track_execution("Pipeline Task"):
                    # Schedule tasks for each text item in the batch
                    loader = TextLoader()
                    future_load = self.client.submit(loader.load_text, text)
                    loaded_text = future_load.result()

                    segmenter = TextSegmenter()
                    future_segment = self.client.submit(segmenter.segment_sentences, loaded_text)
                    sentences = future_segment.result()

                    tokenizer = TextTokenizer()
                    future_tokenize = self.client.submit(tokenizer.tokenize_text, loaded_text)
                    tokens = future_tokenize.result()

                    ner_processor = NERProcessor(self.logger)
                    future_ner = self.client.submit(ner_processor.perform_ner, tokens)
                    entities = future_ner.result()

                    saver = TextSaver()
                    future_save = self.client.submit(
                        saver.save_processed_text, sentences, entities, tokens, output_file
                    )
                    results.append(future_save.result())

                    self.logger.info(f"Processed text and saved to {output_file}")

            except Exception as e:
                self.logger.error(f"Error processing text batch item: {e}")

        return results


    def run_pipeline(self, input_texts, save_filepath):
        """
        Run the entire pipeline for a list of texts in batches.
        """
        try:
            with self.performance_tracker.track_execution("Full Pipeline Execution"):
                self.logger.info("Starting batch processing pipeline.")

                # Use BatchProcessor to process texts in defined batch sizes
                self.batch_processor.process(input_texts, self.process_batch)

                self.logger.info("Batch processing pipeline completed.")
        except Exception as e:
            self.logger.error(f"Error running the full pipeline: {e}")


if __name__ == "__main__":
    # Sample data and output filepath
    sample_texts = ["This is a sample text.", "Another text for processing."]
    sample_output_filepath = "/data/data/processed_output.csv"

    # Assume config_manager is initialized
    config_manager = ConfigManager()
    pipeline_manager = PipelineManager(config_manager)
    pipeline_manager.run_pipeline(sample_texts, sample_output_filepath)
