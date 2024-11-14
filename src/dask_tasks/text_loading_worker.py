from dask.distributed import Client
from src.nlp_pipeline.text_loader import TextLoader
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize Dask client, logger, and performance tracker
client = Client()
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()


def load_text_task(text):
    """
    Load text for processing and track performance.
    """
    loader = TextLoader(logger)

    with perf_tracker.track_execution("Text Loading"):
        logger.info("Starting text loading task.")
        try:
            result = loader.load_text(text)
            logger.info("Text loading completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error loading text: {e}")
            raise


client.register_worker_plugin(load_text_task)

if __name__ == "__main__":
    sample_text = "This is a sample text to load."
    future = client.submit(load_text_task, sample_text)
    print(future.result())
