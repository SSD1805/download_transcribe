
import click
from src.modules.text_processor import TextProcessor

@click.group()
def cli():
    """Command-line interface for text processing tasks."""
    pass

@cli.command()
@click.argument('text')
@click.argument('output_filepath')
def process(text, output_filepath):
    """Process input text and save the output to a specified file."""
    processor = TextProcessor()
    processor.process_text(text, output_filepath)
    click.echo(f"Processed text saved to: {output_filepath}")

if __name__ == '__main__':
    cli()
