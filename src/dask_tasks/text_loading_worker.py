from dask.distributed import Client
from src.pipelines.text.text_loader import TextLoader
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

# Initialize Dask client, logger, and performance tracker
client = Client()



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
