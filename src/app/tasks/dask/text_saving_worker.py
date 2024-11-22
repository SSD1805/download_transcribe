import click
from dask.distributed import Client
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer

# Initialize Dask client
client = Client()


@inject
def save_text_task(
    processed_sentences,
    identified_entities,
    output_filepath,
    saver=Provide[AppContainer.pipeline_component_registry.provide("text_saver")],
    logger=Provide[AppContainer.logger],
    perf_tracker=Provide[AppContainer.performance_tracker],
):
    """
    Save processed text and track performance.

    Args:
        processed_sentences (list): The processed sentences to save.
        identified_entities (list): The identified entities to save.
        output_filepath (str): The output file path.
    """
    with perf_tracker.track_execution("Text Saving"):
        logger.info("Starting text saving task.")
        try:
            saver.save_processed_text(
                processed_sentences, identified_entities, output_filepath
            )
            logger.info(f"Text saved successfully to {output_filepath}.")
        except Exception as e:
            logger.error(f"Error saving text to {output_filepath}: {e}")
            raise


@click.command()
@click.argument("sentences", nargs=-1)
@click.argument("entities", nargs=-1)
@click.argument("output_filepath")
@inject
def main(sentences, entities, output_filepath):
    """Command-line entry for saving text."""
    future = client.submit(save_text_task, sentences, entities, output_filepath)
    click.echo(f"Save completed for file: {output_filepath}")


if __name__ == "__main__":
    # Wire dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])
    main()
