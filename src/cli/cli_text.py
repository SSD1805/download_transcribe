import click
from dependency_injector.wiring import inject, Provide
from infrastructure.dependency_setup import container

@click.group()
def cli():
    """CLI for the Text Processing Pipeline"""
    pass

@cli.command()
@click.option('--input-dir', required=True, help="Directory containing raw text files.")
@inject
def load(input_dir, text_loader=Provide[container.pipeline_component_registry.provide_pipeline_components().get("text_loader")], logger=Provide[container.logger]):
    """Load text files for processing."""
    try:
        logger.info(f"Loading text files from directory: {input_dir}")
        text_loader.load_from_directory(input_dir)
        logger.info(f"Text files loaded from {input_dir}")
    except Exception as e:
        logger.error(f"Failed to load text files from directory {input_dir}: {e}")

@cli.command()
@click.option('--tasks', default="all", help="Tasks to run: tokenization, segmentation, ner.")
@inject
def process(tasks, registry=Provide[container.pipeline_component_registry], logger=Provide[container.logger]):
    """Process text with the specified tasks."""
    try:
        tasks = tasks.split(",")
        registry = registry()  # Resolve the registry
        for task in tasks:
            task_instance = registry.get(task)
            task_instance.run()
            logger.info(f"Completed task: {task}")
    except Exception as e:
        logger.error(f"Failed to process text tasks {tasks}: {e}")

@cli.command()
@click.option('--format', default="csv", help="Output format (csv, json).")
@click.option('--output-dir', required=True, help="Directory to save processed files.")
@inject
def save(format, output_dir, text_saver=Provide[container.pipeline_component_registry.provide_pipeline_components().get("text_saver")], logger=Provide[container.logger]):
    """Save processed text files."""
    try:
        logger.info(f"Saving processed text files to {output_dir} in format: {format}")
        text_saver.save(output_format=format, output_directory=output_dir)
        logger.info(f"Processed text files saved in {output_dir} as {format} files.")
    except Exception as e:
        logger.error(f"Failed to save processed text files in {output_dir}: {e}")

if __name__ == '__main__':
    cli()
