import cli
from src.modules.whisper_ai_fallback import WhisperAIFallback

from src.modules.config_manager import ConfigManager
from src.modules.text_processor import TextProcessor
from src.modules.transcription_manager import TranscriptionManagerWhisperX
from src.pipelines.download.youtube_downloader import YouTubeDownloader
from src.utils.file_utilities import FileManager
from src.utils.structlog_logger import LoggerService

# Get logger and performance tracker from CoreServices
logger = LoggerService.get_instance()
perf_tracker = CoreServices.get_performance_tracker()

# Initialize the logger
from core.settings_registry import SettingsRegistry
from modules.config_manager import ConfigManager
from modules.performance_configurator import PerformanceConfigurator

# Initialize settings instances
config_manager = ConfigManager(config_path="config.yaml")
performance_configurator = PerformanceConfigurator(performance_tracker)

# Register settings with the registries
SettingsRegistry.register("config", config_manager)
SettingsRegistry.register("performance", performance_configurator)


@cli.group()
def cli():
    """YouTube Audio Downloader and Transcriber CLI"""
    pass

@cli.command()
@cli.option('--url', prompt='Enter YouTube URL', help='YouTube video or channel URL to download modules from.')
def download(url):
    """Download modules from YouTube"""
    logger.info(f"Starting download for URL: {url}")
    downloader = YouTubeDownloader()
    downloader.download_video(url)

@cli.command()
@cli.argument('audio_file')
@cli.option('--title', prompt='Enter video title', help='Title for the modules file.')
@cli.option('--use-whisperx', is_flag=True, default=False, help='Use WhisperX for transcription_service.')
@cli.option('--fallback-to-whisper', is_flag=True, default=False, help='Use Whisper AI as a fallback if WhisperX fails.')
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
@cli.option('--directory', default='/data/audio_files', help='Directory to process transcriptions.')
@cli.option('--use-whisperx', is_flag=True, default=False, help='Use WhisperX modules module.')
def process(directory, use_whisperx):
    """Process transcriptions for NER and sentence segmentation"""
    logger.info(f"Processing transcriptions in directory: {directory}")
    if use_whisperx:
        processor = TranscriptionManagerWhisperX()
    else:
        processor = TranscriptionManagerWhisperX()
    processor.process_transcriptions(directory)

    # Use TextProcessor for additional text modules
    text_processor = TextProcessor()
    text_processor.process_texts(directory)

@cli.command()
@cli.option('--config-path', default='config.yaml', help='Path to the configuration file.')
def setup(config_path):
    """Set up configuration for the application"""
    logger.info(f"Setting up configuration from: {config_path}")
    config_manager = ConfigManager(config_path)
    config_manager.load_config()

@cli.command()
@cli.option('--directory', default='/data/audio_files', help='Directory to manage files.')
def manage_files(directory):
    """Run file management tasks"""
    logger.info(f"Managing files in directory: {directory}")
    file_manager = FileManager()
    file_manager.list_files(directory)

if __name__ == '__main__':
    cli()
