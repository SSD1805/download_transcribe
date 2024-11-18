from dask.distributed import Client
from src.pipelines.text.text_saver import TextSaver
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

# Initialize Dask client, logger, and performance tracker
client = Client()



def save_text_task(processed_sentences, identified_entities, output_filepath):
    """
    Save processed text and track performance.
    """
    saver = TextSaver()

    with perf_tracker.track_execution("Text Saving"):
        logger.info("Starting text saving task.")
        try:
            saver.save_processed_text(processed_sentences, identified_entities, output_filepath)
            logger.info(f"Text saved successfully to {output_filepath}.")
        except Exception as e:
            logger.error(f"Error saving text to {output_filepath}: {e}")
            raise


client.register_worker_plugin(save_text_task)

if __name__ == "__main__":
    sentences = ["This is a sentence.", "This is another sentence."]
    entities = [{"text": "Sample", "label": "NOUN"}]
    filepath = "/data/data/processed_text.csv"
    future = client.submit(save_text_task, sentences, entities, filepath)
    print("Save completed.")
