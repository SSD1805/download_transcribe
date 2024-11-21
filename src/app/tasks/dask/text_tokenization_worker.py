from dask.distributed import Client
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer
import click

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
    Tokenize text into words and track performance.
    """
    with perf_tracker.track_execution("Text Tokenization"):
        logger.info("Starting text tokenization task.")
        try:
            result = tokenizer.tokenize_text(text)
            logger.info("Text tokenization completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error during text tokenization: {e}")
            raise


@click.command()
@click.argument("sample_text")
@inject
def main(sample_text: str):
    """Command-line entry for the text tokenization."""
    future = client.submit(tokenize_text_task, sample_text)
    click.echo(f"Tokenization Result: {future.result()}")


if __name__ == "__main__":
    # Wire dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])
    main()
