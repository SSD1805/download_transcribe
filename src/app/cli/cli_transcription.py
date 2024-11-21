import click
from .commands.base_command import BaseCommand
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer

# Command Classes for Transcription Pipeline Tasks

class TranscribeCommand(BaseCommand):
    """
    Command to handle running the transcription pipeline on audio files.
    """

    @inject
    def __init__(self, pipeline=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("transcription_pipeline")],
                 logger=Provide[AppContainer.struct_logger],
                 performance_tracker=Provide[AppContainer.tracking_utility]):
        self.pipeline = pipeline
        self.logger = logger
        self.performance_tracker = performance_tracker

    def execute(self, input_directory, output_directory):
        try:
            self.logger.info(f"Starting transcription for directory: {input_directory}")
            with self.performance_tracker.track_execution("transcription_pipeline"):
                self.pipeline.set_directories(input_directory, output_directory)
                self.pipeline.process_files()
            self.logger.info(f"Transcription completed. Output saved in: {output_directory}")
        except Exception as e:
            self.logger.error(f"Transcription failed for directory {input_directory}: {e}")
            raise

class SaveTranscriptionCommand(BaseCommand):
    """
    Command to handle saving transcription segments to a file.
    """

    @inject
    def __init__(self, saver=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("transcription_saver")],
                 logger=Provide[AppContainer.struct_logger]):
        self.saver = saver
        self.logger = logger

    def execute(self, segments, audio_file, output_directory, format):
        try:
            self.logger.info(f"Saving transcription for audio file: {audio_file} to {output_directory} in format: {format}")
            self.saver.save_transcription(segments, audio_file, format=format)
            self.logger.info(f"Transcription saved for {audio_file} in {output_directory} as {format}")
        except Exception as e:
            self.logger.error(f"Failed to save transcription for {audio_file}: {e}")
            raise

# CLI Commands with Click

@click.group()
def cli():
    """CLI for Transcription Tasks"""
    pass

@cli.command()
@click.argument('input_directory')
@click.argument('output_directory')
@click.pass_context
def transcribe(ctx, input_directory, output_directory):
    """Run the transcription pipeline on audio files."""
    command = ctx.obj.get('transcribe_command')
    command.execute(input_directory, output_directory)

@cli.command()
@click.argument('segments')
@click.argument('audio_file')
@click.argument('output_directory')
@click.option('--format', default='txt', help='Output format: txt or json')
@click.pass_context
def save_transcription(ctx, segments, audio_file, output_directory, format):
    """Save transcription segments to a file."""
    command = ctx.obj.get('save_transcription_command')
    command.execute(segments, audio_file, output_directory, format)

# Main Entry Point
@click.pass_context
def setup_context(ctx):
    """
    Set up the dependency context for CLI commands.
    """
    container = AppContainer()
    ctx.ensure_object(dict)

    # Instantiate command classes and add them to the context
    ctx.obj['transcribe_command'] = TranscribeCommand()
    ctx.obj['save_transcription_command'] = SaveTranscriptionCommand()

# Inject the setup_context to initialize commands
if __name__ == '__main__':
    cli(obj={})  # Initialize with an empty context dictionary and let Click pass it to commands
