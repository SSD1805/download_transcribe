from dask.distributed import Client
from src.nlp_pipeline.text_saver import TextSaver
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize Dask client, logger, and performance tracker
client = Client()
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()


def save_text_task(sentences, entities, filepath):
    """
    Save processed text and track performance.
    """
    saver = TextSaver(logger)

    with perf_tracker.track_execution("Text Saving"):
        logger.info("Starting text saving task.")
        try:
            saver.save_processed_text(sentences, entities, filepath)
            logger.info(f"Text saved successfully to {filepath}.")
        except Exception as e:
            logger.error(f"Error saving text to {filepath}: {e}")
            raise


client.register_worker_plugin(save_text_task)

if __name__ == "__main__":
    sentences = ["This is a sentence.", "This is another sentence."]
    entities = [{"text": "Sample", "label": "NOUN"}]
    filepath = "/app/data/processed_text.csv"
    future = client.submit(save_text_task, sentences, entities, filepath)
    print("Save completed.")
