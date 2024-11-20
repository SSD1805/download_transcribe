from dask.distributed import Client
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer
import click

# Initialize Dask client
client = Client()

@inject
def segment_text_task(
    text: str,
    segmenter=Provide[AppContainer.pipeline_component_registry.provide("text_segmenter")],
    logger=Provide[AppContainer.logger],
    perf_tracker=Provide[AppContainer.performance_tracker]
):
    """
    Segment text into sentences and track performance.
    """
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

@click.command()
@click.argument('sample_text')
@inject
def main(sample_text: str):
    """Command-line entry for the text segmentation."""
    future = client.submit(segment_text_task, sample_text)
    click.echo(f"Segmentation Result: {future.result()}")


if __name__ == "__main__":
    # Wire dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])
    main()
