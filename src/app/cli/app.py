import click
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer

# Refactored CLI Command Classes

class DownloadCommand:
    """
    Command to handle downloading a single video from YouTube.
    """

    @inject
    def __init__(self, downloader=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")],
                 logger=Provide[AppContainer.struct_logger]):
        self.downloader = downloader
        self.logger = logger

    def execute(self, url):
        try:
            self.logger.info(f"Starting download for URL: {url}")
            self.downloader.download_video(url)
            self.logger.info(f"Download completed for URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed to download video from URL {url}: {e}")
            raise

class TranscribeCommand:
    """
    Command to handle transcribing an audio file.
    """

    @inject
    def __init__(self, transcriber=Provide[AppContainer.transcriber],
                 pipeline=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("transcription_pipeline")],
                 logger=Provide[AppContainer.struct_logger],
                 performance_tracker=Provide[AppContainer.tracking_utility]):
        self.transcriber = transcriber
        self.pipeline = pipeline
        self.logger = logger
        self.performance_tracker = performance_tracker

    def execute(self, audio_file, title, use_whisperx, fallback_to_whisper):
        try:
            if use_whisperx:
                self.logger.info(f"Using WhisperX to transcribe audio file: {audio_file}")
                with self.performance_tracker.track_execution("transcription_pipeline"):
                    success = self.pipeline.transcribe_audio(audio_file, title)
                if not success and fallback_to_whisper:
                    self.logger.warning(f"WhisperX failed. Falling back to Whisper AI for audio file: {audio_file}")
                    self.transcriber.transcribe_audio(audio_file, title)
            else:
                self.logger.info(f"Using Whisper AI to transcribe audio file: {audio_file}")
                with self.performance_tracker.track_execution("transcription_pipeline"):
                    self.transcriber.transcribe_audio(audio_file, title)

            self.logger.info(f"Transcription completed for file: {audio_file}")
        except Exception as e:
            self.logger.error(f"Transcription failed for {audio_file}: {e}")
            raise

class BatchProcessCommand:
    """
    Command to handle batch processing tasks.
    """

    @inject
    def __init__(self, batch_processor=Provide[AppContainer.batch_processor],
                 logger=Provide[AppContainer.struct_logger]):
        self.batch_processor = batch_processor
        self.logger = logger

    def execute(self, input_directory, output_directory):
        try:
            self.logger.info(f"Starting batch processing for input directory: {input_directory}")
            self.batch_processor.process(input_directory, output_directory)
            self.logger.info(f"Batch processing completed. Output saved in: {output_directory}")
        except Exception as e:
            self.logger.error(f"Batch processing failed for input directory {input_directory}: {e}")
            raise

# CLI Commands with Click

@click.group()
def cli():
    """YouTube Audio Downloader and Transcriber CLI"""
    pass

@cli.command()
@click.option('--url', prompt='Enter YouTube URL', help='YouTube video or channel URL to download.')
@click.pass_context
def download(ctx, url):
    """Download video from YouTube"""
    command = ctx.obj.get('download_command')
    command.execute(url)

@cli.command()
@click.argument('audio_file')
@click.option('--title', prompt='Enter video title', help='Title for the audio file.')
@click.option('--use-whisperx', is_flag=True, default=False, help='Use WhisperX for transcription.')
@click.option('--fallback-to-whisper', is_flag=True, default=False, help='Use Whisper AI as a fallback if WhisperX fails.')
@click.pass_context
def transcribe(ctx, audio_file, title, use_whisperx, fallback_to_whisper):
    """Transcribe the provided audio file"""
    command = ctx.obj.get('transcribe_command')
    command.execute(audio_file, title, use_whisperx, fallback_to_whisper)

@cli.command()
@click.argument('input_directory')
@click.argument('output_directory')
@click.pass_context
def batch_process(ctx, input_directory, output_directory):
    """Process batch tasks for input directory"""
    command = ctx.obj.get('batch_command')
    command.execute(input_directory, output_directory)

# Main Entry Point

@click.pass_context
def setup_context(ctx):
    """
    Set up the dependency context for CLI commands.
    """
    container = AppContainer()
    ctx.ensure_object(dict)

    # Instantiate command classes and add them to the context
    ctx.obj['download_command'] = container.download_command()
    ctx.obj['transcribe_command'] = container.transcribe_command()
    ctx.obj['batch_command'] = container.batch_command()

# Inject the setup_context to initialize commands
if __name__ == '__main__':
    cli(obj={})  # Initialize with an empty context dictionary and let Click pass it to commands
