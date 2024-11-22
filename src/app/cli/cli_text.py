import click
from src.app.cli.commands.base_command import BaseCommand


@click.group(cls=BaseCommand)
def cli():
    """CLI for the Text Processing Pipeline."""
    pass


@cli.command(cls=BaseCommand)
@click.option("--input-dir", required=True, help="Directory containing raw text files.")
def load(input_dir):
    """Load text files for processing."""
    from src.app.pipelines.text.text_loader import TextLoader
    loader = TextLoader()
    loader.load_from_directory(input_dir)


@cli.command(cls=BaseCommand)
@click.option("--tasks", default="all", help="Tasks to run: tokenization, segmentation, ner.")
def process(tasks):
    """Process text with the specified tasks."""
    from src.app.pipelines.text.text_processor import TextProcessor
    processor = TextProcessor()
    processor.process(tasks)


@cli.command(cls=BaseCommand)
@click.option("--format", default="csv", help="Output format (csv, json).")
@click.option("--output-dir", required=True, help="Directory to save processed files.")
def save(format, output_dir):
    """Save processed text files."""
    from src.app.pipelines.text.text_saver import TextSaver
    saver = TextSaver()
    saver.save(output_format=format, output_directory=output_dir)


if __name__ == "__main__":
    cli()
