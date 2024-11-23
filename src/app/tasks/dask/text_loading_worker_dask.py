import click
from dask.distributed import Client
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer

# Initialize Dask client
client = Client()


@inject
def load_text_task(
    text: str,
    loader=Provide[AppContainer.pipeline_component_registry.provide("text_loader")],
    logger=Provide[AppContainer.logger],
    perf_tracker=Provide[AppContainer.performance_tracker],
):
    """
    Load text_processing for processing and track performance.
    """
    with perf_tracker.track_execution("Text Loading"):
        logger.info("Starting text_processing loading task.")
        try:
            result = loader.load_text(text)
            logger.info("Text loading completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error loading text_processing: {e}")
            raise


@click.command()
@click.argument("sample_text")
@inject
def main(sample_text: str):
    """Command-line entry for loading text_processing."""
    future = client.submit(load_text_task, sample_text)
    click.echo(f"Text Loading Result: {future.result()}")


if __name__ == "__main__":
    # Wire dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])
    main()
