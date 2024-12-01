# Standard Library Imports
import logging

# Third-Party Imports
from dependency_injector import containers, providers

# Application Imports
from src.app.async_tasks.celery import AudioProcessingTask, DownloadTask
from src.app.async_tasks.observers import CoordinatorObserver, LoggerObserver
from src.app.cli import (
    BatchDownloadCommand,
    ConvertAudioCommand,
    DownloadChannelCommand,
    DownloadPlaylistCommand,
    DownloadVideoCommand,
    NormalizeAudioCommand,
    SplitAudioCommand,
    TrimAudioCommand,
)
from src.app.pipelines.audio_processing import (
    AudioConverter,
    AudioNormalizer,
    AudioProcessingPipeline,
    AudioSplitter,
    AudioTrimmer,
)
from src.app.pipelines.text_processing import (
    TextLoader,
    TextSaver,
    TextSegmenter,
    TextTokenizer,
)
from src.app.pipelines.transcription import AudioTranscriber, TranscriptionPipeline
from src.app.utils import ApplicationLogger, PerformanceTracker
from src.infrastructure.registries import ConfigurationRegistry


class AppContainer(containers.DeclarativeContainer):
    """
    Dependency injection container for the application.
    """

    # Configuration Registry (shared across all pipelines and async_tasks)
    configuration_registry = providers.Singleton(ConfigurationRegistry)

    # Shared Utilities
    logger = providers.Singleton(ApplicationLogger.get_logger)
    performance_tracker = providers.Singleton(PerformanceTracker)

    # Observers
    logger_observer = providers.Factory(LoggerObserver, logger=logger)
    coordinator_observer = providers.Factory(CoordinatorObserver, logger=logger)

    # Audio Pipeline Components
    audio_converter = providers.Singleton(AudioConverter)
    audio_normalizer = providers.Singleton(AudioNormalizer)
    audio_splitter = providers.Singleton(AudioSplitter)
    audio_trimmer = providers.Singleton(AudioTrimmer)

    # Audio Processing Pipeline
    audio_processing_pipeline = providers.Singleton(
        AudioProcessingPipeline,
        converter=audio_converter,
        normalizer=audio_normalizer,
        splitter=audio_splitter,
        trimmer=audio_trimmer,
    )

    # Transcription Pipeline Components
    transcription_pipeline = providers.Singleton(TranscriptionPipeline)
    transcriber = providers.Singleton(AudioTranscriber)

    # Text Processing Components
    text_loader = providers.Singleton(TextLoader)
    text_segmenter = providers.Singleton(TextSegmenter)
    text_tokenizer = providers.Singleton(TextTokenizer)
    text_saver = providers.Singleton(TextSaver)

    # Tasks
    audio_processing_task = providers.Factory(
        AudioProcessingTask,
        pipeline=audio_processing_pipeline,
        logger_observer=logger_observer,
        coordinator_observer=coordinator_observer,
    )
    download_task = providers.Factory(
        DownloadTask,
        logger_observer=logger_observer,
        coordinator_observer=coordinator_observer,
    )

    # CLI Commands
    audio_commands = providers.Factory(
        normalize_command=NormalizeAudioCommand,
        split_command=SplitAudioCommand,
        trim_command=TrimAudioCommand,
        convert_command=ConvertAudioCommand,
    )
    download_commands = providers.Factory(
        download_command=DownloadVideoCommand,
        channel_command=DownloadChannelCommand,
        playlist_command=DownloadPlaylistCommand,
        batch_command=BatchDownloadCommand,
    )

    # Structlog Configuration
    structlog_configuration = providers.Resource(ApplicationLogger.configure_structlog)


# Initialize Logging
logger = logging.getLogger(__name__)
logger.info("AppContainer initialized successfully.")
