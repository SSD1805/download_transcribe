from dask.distributed import Client
from src.pipelines.text.text_tokenizer import TextTokenizer
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

# Initialize Dask client, logger, and performance tracker
client = Client()



def tokenize_text_task(text):
    """
    Tokenize text into words and track performance.
    """
    tokenizer = TextTokenizer(logger)

    with perf_tracker.track_execution("Text Tokenization"):
        logger.info("Starting text tokenization task.")
        try:
            result = tokenizer.tokenize_text(text)
            logger.info("Text tokenization completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error during text tokenization: {e}")
            raise


client.register_worker_plugin(tokenize_text_task)

if __name__ == "__main__":
    sample_text = "This is a sample text for tokenization."
    future = client.submit(tokenize_text_task, sample_text)
    print(future.result())
