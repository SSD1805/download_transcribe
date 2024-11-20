from dask.distributed import Client
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer
from src.pipelines.text.ner_processor import NERProcessor


# Initialize Dask client
client = Client()

@inject
def ner_task(
    text: str,
    logger=Provide[AppContainer.logger],
    perf_tracker=Provide[AppContainer.performance_tracker],
):
    """
    Perform Named Entity Recognition (NER) on text and track performance.

    Args:
        text (str): The text on which to perform NER.
        logger: Logger instance to log information.
        perf_tracker: Performance tracker to track execution time.
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


# Register the task function with Dask as a worker plugin
client.register_worker_plugin(ner_task)

if __name__ == "__main__":
    # Wire the dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])

    # Example usage: submitting an NER task
    sample_text = "Elon Musk founded SpaceX and Tesla in California."
    future = client.submit(ner_task, sample_text)
    print(future.result())
