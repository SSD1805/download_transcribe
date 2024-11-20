from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer
import click

class TextProcessor:
    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        """
        Initialize the TextProcessor.

        Args:
            logger: The logger instance from the AppContainer.
        """
        self.logger = logger

    def process_text(self, text, output_filepath):
        """
        Processes the input text and saves it to the specified file.

        Args:
            text (str): The input text to process.
            output_filepath (str): Path to save the processed text.
        """
        with open(output_filepath, 'w') as f:
            processed_text = text.upper()  # Example processing
            f.write(processed_text)
        self.logger.info(f"Processed text saved to: {output_filepath}")


@click.group()
def cli():
    """Command-line interface for text processing tasks."""
    pass


@cli.command()
@click.argument('text')
@click.argument('output_filepath')
@inject
def process(
    text,
    output_filepath,
    perf_tracker=Provide[AppContainer.performance_tracker],
    logger=Provide[AppContainer.logger],
    text_processor=Provide[AppContainer.pipeline_component_registry.provide("text_processor")]
):
    """Process input text and save the output to a specified file."""
    try:
        with perf_tracker.track_execution("Text Processing Command"):
            logger.info(f"Starting text processing for output file: {output_filepath}")
            text_processor.process_text(text, output_filepath)
            click.echo(f"Processed text saved to: {output_filepath}")
    except Exception as e:
        logger.error(f"Failed to process text: {e}")
        click.echo(f"Error: Failed to process text. Check logs for more details.")


if __name__ == '__main__':
    # Initialize the dependency container
    container = AppContainer()
    container.wire(modules=[__name__])
    cli()
