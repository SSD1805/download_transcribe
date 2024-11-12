import click
from src.download_pipeline.youtube_downloader import YouTubeDownloader
from src.modules.audio_handler import Transcriber
from src.modules.whisper_ai_fallback import WhisperAIFallback
from src.modules.transcription_manager import TranscriptionManagerWhisperX
from src.core.file_manager import FileManager
from src.modules.text_processor import TextProcessor
from src.modules.config_manager import ConfigManager
from src.core.logger_manager import LoggerManager

# Initialize the logger
log_manager = LoggerManager()
logger = log_manager.get_logger()

@click.group()
def cli():
    """YouTube Audio Downloader and Transcriber CLI"""
    pass

@cli.command()
@click.option('--url', prompt='Enter YouTube URL', help='YouTube video or channel URL to download modules from.')
def download(url):
    """Download modules from YouTube"""
    logger.info(f"Starting download for URL: {url}")
    downloader = YouTubeDownloader()
    downloader.download_video(url)

@cli.command()
@click.argument('audio_file')
@click.option('--title', prompt='Enter video title', help='Title for the modules file.')
@click.option('--use-whisperx', is_flag=True, default=False, help='Use WhisperX for transcription_pipeline.')
@click.option('--fallback-to-whisper', is_flag=True, default=False, help='Use Whisper AI as a fallback if WhisperX fails.')
def transcribe(audio_file, title, use_whisperx, fallback_to_whisper):
    """Transcribe the provided modules file"""
    if use_whisperx:
        logger.info(f"Using WhisperX to transcribe modules file: {audio_file}")
        transcriber = WhisperXTranscriber()
        success = transcriber.transcribe_audio(audio_file, title)
        if not success and fallback_to_whisper:
            logger.warning(f"WhisperX failed. Falling back to Whisper AI for modules file: {audio_file}")
            fallback_transcriber = WhisperAIFallback()
            fallback_transcriber.transcribe_audio(audio_file, title)
    else:
        logger.info(f"Using Whisper AI to transcribe modules file: {audio_file}")
        transcriber = Transcriber()
        transcriber.transcribe_audio(audio_file, title)

@cli.command()
@click.option('--directory', default='/app/audio_files', help='Directory to process transcriptions.')
@click.option('--use-whisperx', is_flag=True, default=False, help='Use WhisperX modules module.')
def process(directory, use_whisperx):
    """Process transcriptions for NER and sentence segmentation"""
    logger.info(f"Processing transcriptions in directory: {directory}")
    if use_whisperx:
        processor = TranscriptionManagerWhisperX()
    else:
        processor = TranscriptionManager()
    processor.process_transcriptions(directory)

    # Use TextProcessor for additional text modules
    text_processor = TextProcessor()
    text_processor.process_texts(directory)

@cli.command()
@click.option('--config-path', default='config.yaml', help='Path to the configuration file.')
def setup(config_path):
    """Set up configuration for the application"""
    logger.info(f"Setting up configuration from: {config_path}")
    config_manager = ConfigManager(config_path)
    config_manager.load_config()

@cli.command()
@click.option('--directory', default='/app/audio_files', help='Directory to manage files.')
def manage_files(directory):
    """Run file management tasks"""
    logger.info(f"Managing files in directory: {directory}")
    file_manager = FileManager()
    file_manager.list_files(directory)

if __name__ == '__main__':
    cli()