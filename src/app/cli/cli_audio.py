import click
from .commands.base_command import BaseCommand
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer

# Command Classes for Different Audio Tasks

class NormalizeAudioCommand(BaseCommand):
    """
    Command to handle audio normalization.
    """

    @inject
    def __init__(self, handler=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[AppContainer.struct_logger]):
        self.handler = handler
        self.logger = logger

    def execute(self, input_file, output_file):
        try:
            self.logger.info(f"Normalizing audio file: {input_file}")
            result = self.handler.normalize_audio(input_file, output_file)
            self.logger.info(f"Normalization completed. Output file: {result}")
        except Exception as e:
            self.logger.error(f"Failed to normalize audio file {input_file}: {e}")
            raise

class SplitAudioCommand(BaseCommand):
    """
    Command to handle audio splitting.
    """

    @inject
    def __init__(self, handler=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[AppContainer.struct_logger]):
        self.handler = handler
        self.logger = logger

    def execute(self, input_file, chunk_duration, output_file_prefix):
        try:
            self.logger.info(f"Splitting audio file: {input_file} into chunks of {chunk_duration} seconds.")
            result = self.handler.split_audio(input_file, chunk_duration, output_file_prefix)
            self.logger.info(f"Audio split into {len(result)} chunks.")
        except Exception as e:
            self.logger.error(f"Failed to split audio file {input_file}: {e}")
            raise

class TrimAudioCommand(BaseCommand):
    """
    Command to handle trimming silence from audio files.
    """

    @inject
    def __init__(self, handler=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[AppContainer.struct_logger]):
        self.handler = handler
        self.logger = logger

    def execute(self, input_file, output_file, silence_thresh):
        try:
            self.logger.info(f"Trimming silence from audio file: {input_file}")
            result = self.handler.trim_audio(input_file, output_file, silence_thresh)
            self.logger.info(f"Silence trimmed. Output file: {result}")
        except Exception as e:
            self.logger.error(f"Failed to trim audio file {input_file}: {e}")
            raise

class ConvertAudioCommand(BaseCommand):
    """
    Command to handle converting audio formats.
    """

    @inject
    def __init__(self, handler=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[AppContainer.struct_logger]):
        self.handler = handler
        self.logger = logger

    def execute(self, input_file, output_file, target_format):
        try:
            self.logger.info(f"Converting audio file: {input_file} to format: {target_format}")
            result = self.handler.convert_audio(input_file, output_file, target_format)
            self.logger.info(f"Conversion completed. Output file: {result}")
        except Exception as e:
            self.logger.error(f"Failed to convert audio file {input_file}: {e}")
            raise

# Other command classes like running the transcription pipeline can follow a similar pattern.

# CLI Commands with Click

@click.group()
def cli():
    """CLI for Audio Processing Tasks"""
    pass

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.pass_context
def normalize(ctx, input_file, output_file):
    """Normalize an audio file."""
    command = ctx.obj.get('normalize_command')
    command.execute(input_file, output_file)

@cli.command()
@click.argument('input_file')
@click.argument('chunk_duration', type=int)
@click.argument('output_file_prefix')
@click.pass_context
def split(ctx, input_file, chunk_duration, output_file_prefix):
    """Split an audio file into smaller chunks."""
    command = ctx.obj.get('split_command')
    command.execute(input_file, chunk_duration, output_file_prefix)

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--silence-thresh', default=-40, help='Silence threshold in dBFS.')
@click.pass_context
def trim(ctx, input_file, output_file, silence_thresh):
    """Trim silence from an audio file."""
    command = ctx.obj.get('trim_command')
    command.execute(input_file, output_file, silence_thresh)

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--target-format', default='wav', help='Target format for audio conversion.')
@click.pass_context
def convert(ctx, input_file, output_file, target_format):
    """Convert an audio file to a specified format."""
    command = ctx.obj.get('convert_command')
    command.execute(input_file, output_file, target_format)

# Main Entry Point
@click.pass_context
def setup_context(ctx):
    """
    Set up the dependency context for CLI commands.
    """
    container = AppContainer()
    ctx.ensure_object(dict)

    # Instantiate command classes and add them to the context
    ctx.obj['normalize_command'] = NormalizeAudioCommand()
    ctx.obj['split_command'] = SplitAudioCommand()
    ctx.obj['trim_command'] = TrimAudioCommand()
    ctx.obj['convert_command'] = ConvertAudioCommand()

# Inject the setup_context to initialize commands
if __name__ == '__main__':
    cli(obj={})  # Initialize with an empty context dictionary and let Click pass it to commands
