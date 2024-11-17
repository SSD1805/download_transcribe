import click
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


class TextProcessor:
    def process_text(self, text, output_filepath):
        """
        Processes the input text and saves it to the specified file.
        """
        with open(output_filepath, 'w') as f:
            f.write(text.upper())  # Example processing

@click.group()
def cli():
    """Command-line interface for text processing tasks."""
    pass

@cli.command()
@click.argument('text')
@click.argument('output_filepath')
def process(text, output_filepath):
    """Process input text and save the output to a specified file."""
    try:
        with perf_tracker.track_execution("Text Processing Command"):
            logger.info(f"Starting text processing for output file: {output_filepath}")
            processor = TextProcessor()
            processor.process_text(text, output_filepath)
            logger.info(f"Processed text saved to: {output_filepath}")
            click.echo(f"Processed text saved to: {output_filepath}")
    except Exception as e:
        logger.error(f"Failed to process text: {e}")
        click.echo(f"Error: Failed to process text. Check logs for more details.")

if __name__ == '__main__':
    cli()