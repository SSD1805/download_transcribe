from dask.distributed import Client
from src.pipelines.text.text_segmenter import TextSegmenter
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

# Initialize Dask client, logger, and performance tracker
client = Client()



def segment_text_task(text):
    """
    Segment text into sentences and track performance.
    """
    segmenter = TextSegmenter(logger)

    with perf_tracker.track_execution("Text Segmentation"):
        logger.info("Starting text segmentation task.")
        try:
            result = segmenter.segment_sentences(text)
            logger.info("Text segmentation completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error during text segmentation: {e}")
            raise


client.register_worker_plugin(segment_text_task)

if __name__ == "__main__":
    sample_text = "This is a sample text. It contains two sentences."
    future = client.submit(segment_text_task, sample_text)
    print(future.result())
