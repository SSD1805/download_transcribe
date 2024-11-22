from dask.distributed import Client
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class PipelineManager:
    @inject
    def __init__(
        self,
        config_manager=Provide[AppContainer.configuration_registry],
        logger=Provide[AppContainer.logger],
        perf_tracker=Provide[AppContainer.performance_tracker],
        memory_monitor=Provide[AppContainer.memory_monitor],
        batch_processor=Provide[AppContainer.batch_processor],
    ):
        """
        Initialize PipelineManager with injected dependencies.

        Args:
            config_manager: The configuration manager instance.
            logger: Logger instance for logging.
            perf_tracker: Performance tracker instance for tracking task performance.
            memory_monitor: Memory monitor instance.
            batch_processor: Batch processor instance.
        """
        self.config_manager = config_manager
        self.logger = logger
        self.performance_tracker = perf_tracker
        self.memory_monitor = memory_monitor
        self.client = Client("tcp://dask_scheduler:8786")  # Connect to Dask scheduler
        self.batch_processor = batch_processor

    @inject
    def process_batch(
        self,
        text_batch,
        output_file,
        text_loader=Provide[
            AppContainer.pipeline_component_registry.provide("text_loader")
        ],
        text_segmenter=Provide[
            AppContainer.pipeline_component_registry.provide("text_segmenter")
        ],
        text_tokenizer=Provide[
            AppContainer.pipeline_component_registry.provide("text_tokenizer")
        ],
        ner_processor=Provide[
            AppContainer.pipeline_component_registry.provide("ner_processor")
        ],
        text_saver=Provide[
            AppContainer.pipeline_component_registry.provide("text_saver")
        ],
    ):
        """
        Process a batch of texts, including loading, segmenting, tokenizing, NER, and saving results.
        """
        results = []

        # Process each item in the batch
        for text in text_batch:
            try:
                with self.performance_tracker.track_execution("Pipeline Task"):
                    # Schedule tasks for each text item in the batch
                    future_load = self.client.submit(text_loader.load_text, text)
                    loaded_text = future_load.result()

                    future_segment = self.client.submit(
                        text_segmenter.segment_sentences, loaded_text
                    )
                    sentences = future_segment.result()

                    future_tokenize = self.client.submit(
                        text_tokenizer.tokenize_text, loaded_text
                    )
                    tokens = future_tokenize.result()

                    future_ner = self.client.submit(ner_processor.perform_ner, tokens)
                    entities = future_ner.result()

                    future_save = self.client.submit(
                        text_saver.save_processed_text,
                        sentences,
                        entities,
                        tokens,
                        output_file,
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
                self.batch_processor.process(
                    lambda batch: self.process_batch(batch, save_filepath), input_texts
                )

                self.logger.info("Batch processing pipeline completed.")
        except Exception as e:
            self.logger.error(f"Error running the full pipeline: {e}")


if __name__ == "__main__":
    # Wire dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])

    # Sample data and output filepath
    sample_texts = ["This is a sample text.", "Another text for processing."]
    sample_output_filepath = "/data/data/processed_output.csv"

    # Initialize the pipeline manager
    pipeline_manager = PipelineManager()
    pipeline_manager.run_pipeline(sample_texts, sample_output_filepath)
