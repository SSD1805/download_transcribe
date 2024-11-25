# src/infrastructure/app/app_container.py
from dependency_injector import containers, providers

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
from src.app.tasks.celery import AudioProcessingTask, DownloadTask
from src.app.tasks.observers import CoordinatorObserver, LoggerObserver
from src.app.utils import ApplicationLogger, PerformanceTracker


class AppContainer(containers.DeclarativeContainer):
    """
    Dependency injection container for the application.
    """

    # Configuration Registry (shared across all pipelines and tasks)
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

    # CLI Commands (if needed)
    audio_commands = providers.Factory(
        NormalizeAudioCommand,
        split_command=SplitAudioCommand,
        trim_command=TrimAudioCommand,
        convert_command=ConvertAudioCommand,
    )
    download_commands = providers.Factory(
        DownloadVideoCommand,
        channel_command=DownloadChannelCommand,
        playlist_command=DownloadPlaylistCommand,
        batch_command=BatchDownloadCommand,
    )

    # Structlog Configuration (delegated to a utility function)
    structlog_configuration = providers.Resource(ApplicationLogger.configure_structlog)
