import click
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer


@click.group()
def cli():
    """CLI for the Text Processing Pipeline"""
    pass


@cli.command()
@click.option('--input-dir', required=True, help="Directory containing raw text files.")
@inject
def load(input_dir, text_loader=Provide[AppContainer.pipeline_component_registry.provide("text_loader")]):
    """Load text files for processing."""
    text_loader.load_from_directory(input_dir)
    click.echo(f"Loaded text files from {input_dir}")


@cli.command()
@click.option('--tasks', default="all", help="Tasks to run: tokenization, segmentation, ner.")
@inject
def process(tasks, registry=Provide[AppContainer.pipeline_component_registry]):
    """Process text with the specified tasks."""
    tasks = tasks.split(",")
    registry = registry()  # Resolve the registry
    for task in tasks:
        task_instance = registry.get(task)
        task_instance.run()
        click.echo(f"Completed task: {task}")


@cli.command()
@click.option('--format', default="csv", help="Output format (csv, json).")
@click.option('--output-dir', required=True, help="Directory to save processed files.")
@inject
def save(format, output_dir, text_saver=Provide[AppContainer.pipeline_component_registry.provide("text_saver")]):
    """Save processed text files."""
    text_saver.save(output_format=format, output_directory=output_dir)
    click.echo(f"Processed text saved in {output_dir} as {format} files.")


if __name__ == '__main__':
    # Initialize the container
    container = AppContainer()
    container.wire(modules=[__name__])

    cli()
