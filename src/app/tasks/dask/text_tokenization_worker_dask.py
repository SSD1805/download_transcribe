import click
from dask.distributed import Client
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer

# Initialize Dask client
client = Client()


@inject
def tokenize_text_task(
    text: str,
    tokenizer=Provide[
        AppContainer.pipeline_component_registry.provide("text_tokenizer")
    ],
    logger=Provide[AppContainer.logger],
    perf_tracker=Provide[AppContainer.performance_tracker],
):
    """
    Tokenize text_processing into words and track performance.
    """
    with perf_tracker.track_execution("Text Tokenization"):
        logger.info("Starting text_processing tokenization task.")
        try:
            result = tokenizer.tokenize_text(text)
            logger.info("Text tokenization completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error during text_processing tokenization: {e}")
            raise


@click.command()
@click.argument("sample_text")
@inject
def main(sample_text: str):
    """Command-line entry for the text_processing tokenization."""
    future = client.submit(tokenize_text_task, sample_text)
    click.echo(f"Tokenization Result: {future.result()}")


if __name__ == "__main__":
    # Wire dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])
    main()
