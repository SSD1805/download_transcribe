import click
from .commands.base_command import BaseCommand
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer

# Command Classes for Text Processing Pipeline

class LoadTextCommand(BaseCommand):
    """
    Command to handle loading text files from a directory.
    """

    @inject
    def __init__(self, text_loader=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("text_loader")], logger=Provide[AppContainer.struct_logger]):
        self.text_loader = text_loader
        self.logger = logger

    def execute(self, input_dir):
        try:
            self.logger.info(f"Loading text files from directory: {input_dir}")
            self.text_loader.load_from_directory(input_dir)
            self.logger.info(f"Text files loaded from {input_dir}")
        except Exception as e:
            self.logger.error(f"Failed to load text files from directory {input_dir}: {e}")
            raise

class ProcessTextCommand(BaseCommand):
    """
    Command to handle processing text with specified tasks.
    """

    @inject
    def __init__(self, registry=Provide[AppContainer.pipeline_component_registry], logger=Provide[AppContainer.struct_logger]):
        self.registry = registry
        self.logger = logger

    def execute(self, tasks):
        try:
            tasks = tasks.split(",")
            registry_instance = self.registry()
            for task in tasks:
                task_instance = registry_instance.get(task)
                task_instance.run()
                self.logger.info(f"Completed task: {task}")
        except Exception as e:
            self.logger.error(f"Failed to process text tasks {tasks}: {e}")
            raise

class SaveTextCommand(BaseCommand):
    """
    Command to handle saving processed text files.
    """

    @inject
    def __init__(self, text_saver=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("text_saver")], logger=Provide[AppContainer.struct_logger]):
        self.text_saver = text_saver
        self.logger = logger

    def execute(self, format, output_dir):
        try:
            self.logger.info(f"Saving processed text files to {output_dir} in format: {format}")
            self.text_saver.save(output_format=format, output_directory=output_dir)
            self.logger.info(f"Processed text files saved in {output_dir} as {format} files.")
        except Exception as e:
            self.logger.error(f"Failed to save processed text files in {output_dir}: {e}")
            raise

# CLI Commands with Click

@click.group()
def cli():
    """CLI for the Text Processing Pipeline"""
    pass

@cli.command()
@click.option('--input-dir', required=True, help="Directory containing raw text files.")
@click.pass_context
def load(ctx, input_dir):
    """Load text files for processing."""
    command = ctx.obj.get('load_command')
    command.execute(input_dir)

@cli.command()
@click.option('--tasks', default="all", help="Tasks to run: tokenization, segmentation, ner.")
@click.pass_context
def process(ctx, tasks):
    """Process text with the specified tasks."""
    command = ctx.obj.get('process_command')
    command.execute(tasks)

@cli.command()
@click.option('--format', default="csv", help="Output format (csv, json).")
@click.option('--output-dir', required=True, help="Directory to save processed files.")
@click.pass_context
def save(ctx, format, output_dir):
    """Save processed text files."""
    command = ctx.obj.get('save_command')
    command.execute(format, output_dir)

# Main Entry Point
@click.pass_context
def setup_context(ctx):
    """
    Set up the dependency context for CLI commands.
    """
    container = AppContainer()
    ctx.ensure_object(dict)

    # Instantiate command classes and add them to the context
    ctx.obj['load_command'] = LoadTextCommand()
    ctx.obj['process_command'] = ProcessTextCommand()
    ctx.obj['save_command'] = SaveTextCommand()

# Inject the setup_context to initialize commands
if __name__ == '__main__':
    cli(obj={})  # Initialize with an empty context dictionary and let Click pass it to commands
