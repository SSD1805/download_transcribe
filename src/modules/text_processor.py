from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker
import click

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

class TextProcessor:
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
        logger.info(f"Processed text saved to: {output_filepath}")

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
            click.echo(f"Processed text saved to: {output_filepath}")
    except Exception as e:
        logger.error(f"Failed to process text: {e}")
        click.echo(f"Error: Failed to process text. Check logs for more details.")

if __name__ == '__main__':
    cli()
