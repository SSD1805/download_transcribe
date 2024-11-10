import click
from src.modules.youtube_downloader import YouTubeDownloader
from src.modules.transcriber import Transcriber
from src.modules.transcription_manager import TranscriptionManager
from src.modules.file_manager import FileManager
from src.modules.text_processor import TextProcessor
from src.modules.config_manager import ConfigManager
from src.modules.logger import LoggerManager

# Initialize the logger
log_manager = LoggerManager()
logger = log_manager.get_logger()

@click.group()
def cli():
    """YouTube Audio Downloader and Transcriber CLI"""
    pass

@cli.command()
@click.option('--url', prompt='Enter YouTube URL', help='YouTube video or channel URL to download audio from.')
def download(url):
    """Download audio from YouTube"""
    logger.info(f"Starting download for URL: {url}")
    downloader = YouTubeDownloader()
    downloader.download_video(url)

@cli.command()
@click.argument('audio_file')
@click.option('--title', prompt='Enter video title', help='Title for the audio file.')
def transcribe(audio_file, title):
    """Transcribe the provided audio file"""
    logger.info(f"Transcribing audio file: {audio_file}")
    transcriber = Transcriber()
    transcriber.transcribe_audio(audio_file, title)

@cli.command()
@click.option('--directory', default='/app/audio_files', help='Directory to process transcriptions.')
def process(directory):
    """Process transcriptions for NER and sentence segmentation"""
    logger.info(f"Processing transcriptions in directory: {directory}")
    processor = TranscriptionManager()
    processor.process_transcriptions(directory)

    # Use TextProcessor for additional text processing
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