### Improved app.py with Dependency Setup Integration ###
import click
from infrastructure.dependency_setup import container, di_inject, di_Provide
from src.utils.structlog_logger import StructLogger
from src.utils.tracking_utilities import PerformanceTracker

# Get logger and performance tracker from the container
logger = StructLogger.get_logger()
performance_tracker = PerformanceTracker.get_instance()

@click.group()
def cli():
    """YouTube Audio Downloader and Transcriber CLI"""
    pass

@cli.command()
@click.option('--url', prompt='Enter YouTube URL', help='YouTube video or channel URL to download.')
@di_inject
def download(url, downloader=di_Provide[container.pipeline_component_registry.provide("youtube_downloader")]):
    """Download video from YouTube"""
    try:
        logger.info(f"Starting download for URL: {url}")
        downloader.download_video(url)
        logger.info(f"Download completed for URL: {url}")
    except Exception as e:
        logger.error(f"Failed to download video: {e}")

@cli.command()
@click.argument('audio_file')
@click.option('--title', prompt='Enter video title', help='Title for the audio file.')
@click.option('--use-whisperx', is_flag=True, default=False, help='Use WhisperX for transcription.')
@click.option('--fallback-to-whisper', is_flag=True, default=False, help='Use Whisper AI as a fallback if WhisperX fails.')
@di_inject
def transcribe(audio_file, title, use_whisperx, fallback_to_whisper, transcriber=di_Provide[container.transcriber]):
    """Transcribe the provided audio file"""
    try:
        if use_whisperx:
            logger.info(f"Using WhisperX to transcribe audio file: {audio_file}")
            whisperx_transcriber = di_Provide[container.pipeline_component_registry.provide("transcription_pipeline")]()
            success = whisperx_transcriber.transcribe_audio(audio_file, title)
            if not success and fallback_to_whisper:
                logger.warning(f"WhisperX failed. Falling back to Whisper AI for audio file: {audio_file}")
                transcriber.transcribe_audio(audio_file, title)
        else:
            logger.info(f"Using Whisper AI to transcribe audio file: {audio_file}")
            transcriber.transcribe_audio(audio_file, title)
        logger.info(f"Transcription completed for file: {audio_file}")
    except Exception as e:
        logger.error(f"Transcription failed for {audio_file}: {e}")

# Other command definitions follow the same pattern...

if __name__ == '__main__':
    cli()


