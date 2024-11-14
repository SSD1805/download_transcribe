from dask.distributed import Client
from src.nlp_pipeline.ner_processor import NERProcessor
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize Dask client, logger, and performance tracker
client = Client()
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()


def ner_task(text):
    """
    Perform Named Entity Recognition (NER) on text and track performance.
    """
    ner_processor = NERProcessor(logger)

    with perf_tracker.track_execution("Named Entity Recognition"):
        logger.info("Starting Named Entity Recognition task.")
        try:
            result = ner_processor.perform_ner(text)
            logger.info("NER task completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error during NER task: {e}")
            raise


client.register_worker_plugin(ner_task)

if __name__ == "__main__":
    sample_text = "Elon Musk founded SpaceX and Tesla in California."
    future = client.submit(ner_task, sample_text)
    print(future.result())
