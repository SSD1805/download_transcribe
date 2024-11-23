import click
from src.app.cli.commands.base_command import BaseCommand


@click.group()
def cli():
    """CLI for the Text Processing Pipeline."""
    pass


@cli.command(cls=BaseCommand)
@click.option("--input-dir", required=True, help="Directory containing raw text files.")
def load(ctx, input_dir):
    """
    Load text files for processing.
    """
    file_utility = ctx.command.file_utility
    text_handler = ctx.command.text_handler

    files = file_utility.list_files(input_dir, extensions=(".txt",))
    for file in files:
        text_handler.load(file)

    click.echo(f"Loaded files from {input_dir}.")


@cli.command(cls=BaseCommand)
@click.option("--tasks", default="all", help="Tasks to run: tokenization, segmentation, ner.")
def process(ctx, tasks):
    """
    Process text with the specified tasks.
    """
    text_handler = ctx.command.text_handler
    text_handler.process_tasks(tasks)

    click.echo(f"Processed tasks: {tasks}.")


@cli.command(cls=BaseCommand)
@click.option("--output-dir", required=True, help="Directory to save processed files.")
@click.option("--format", default="csv", help="Output format (csv, json).")
def save(ctx, output_dir, format):
    """
    Save processed text files.
    """
    file_utility = ctx.command.file_utility
    text_handler = ctx.command.text_handler

    processed_data = text_handler.get_processed_data()
    for index, data in enumerate(processed_data):
        file_path = f"{output_dir}/processed_file_{index}.{format}"
        file_utility.save_file(data.encode(), file_path)

    click.echo(f"Saved files to {output_dir} in {format} format.")


if __name__ == "__main__":
    from src.infrastructure.app.app_container import AppContainer

    container = AppContainer()
    container.wire(modules=[__name__])
    cli()
