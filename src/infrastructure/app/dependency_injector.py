import logging

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

# Import Tasks, CLI Modules, Registries, Pipeline Managers, etc.
from src.app.async_tasks.celery import (
    CleanupTasks,
    DownloadTasks,
    SharedTasks,
    TranscriptionTasks,
)
from src.app.async_tasks.dask import (
    AudioConversionWorker,
    TextProcessingWorker,  # Ensure this exists
    TranscriptionWorker,
)
from src.app.cli import (
    BaseCommand,
    CliAudio,
    CliDownload,
    CliText,
    CliTranscription,
)
from src.app.infrastructure.registries import (
    ConfigurationRegistry,
    GenericRegistry,
    ModelRegistry,
    PipelineRegistry,
)
from src.app.modules import (
    AudioHandler,
    ConfigManager,
    DownloadCoordinator,
    PipelineManager,
    TextHandler,
    TranscriptionManager,
)
from src.app.pipelines.audio_processing import AudioConverter
from src.app.pipelines.download import (
    DownloadHandler,
    YoutubeDownloader,
)
from src.app.pipelines.text_processing import (
    NERProcessor,
    TextLoader,
    TextProcessor,
    TextSaver,
    TextSegmenter,
    TextTokenizer,
)
from src.app.pipelines.transcription import (
    AudioProcessingPipeline,
    AudioTranscriber,
    TranscriptionPipeline,
    TranscriptionSaver,
)

# Import Utilities and Dependencies
from src.app.utils.application_logger import ApplicationLogger
from src.app.utils.concurrency_utilities import (
    ConcurrencyUtilities,  # Ensure this exists
)
from src.app.utils.file_utilities import FileUtilities  # Ensure this exists
from src.app.utils.tracking_utilities import TrackingUtilities  # Ensure this exists


# Define the Dependency Injection Container
class AppContainer(containers.DeclarativeContainer):
    """Dependency Injection Container for the application."""

    # Core Services and Registries
    configuration_registry = providers.Singleton(ConfigurationRegistry)
    model_registry = providers.Singleton(ModelRegistry)
    pipeline_registry = providers.Singleton(PipelineRegistry)
    generic_registry = providers.Singleton(GenericRegistry)

    # Managers
    config_manager = providers.Singleton(ConfigManager)
    pipeline_manager = providers.Singleton(PipelineManager)
    transcription_manager = providers.Singleton(TranscriptionManager)
    download_coordinator = providers.Singleton(DownloadCoordinator)
    audio_handler = providers.Singleton(AudioHandler)
    text_handler = providers.Singleton(TextHandler)

    # Utilities
    structlog_logger = providers.Singleton(ApplicationLogger)  # Updated
    tracking_utilities = providers.Singleton(TrackingUtilities)  # Updated
    file_utilities = providers.Singleton(FileUtilities)  # Updated
    concurrency_utilities = providers.Singleton(ConcurrencyUtilities)  # Updated

    # CLI Commands
    cli_audio = providers.Singleton(CliAudio)
    cli_download = providers.Singleton(CliDownload)
    cli_text = providers.Singleton(CliText)
    cli_transcription = providers.Singleton(CliTranscription)
    base_command = providers.Singleton(BaseCommand)

    # Pipeline Components
    transcription_pipeline = providers.Singleton(TranscriptionPipeline)
    audio_transcriber = providers.Singleton(AudioTranscriber)
    transcription_saver = providers.Singleton(TranscriptionSaver)
    audio_processing_pipeline = providers.Singleton(AudioProcessingPipeline)
    youtube_downloader = providers.Singleton(YoutubeDownloader)
    download_handler = providers.Singleton(DownloadHandler)
    audio_converter = providers.Singleton(AudioConverter)
    text_loader = providers.Singleton(TextLoader)
    text_saver = providers.Singleton(TextSaver)
    ner_processor = providers.Singleton(NERProcessor)
    text_segmenter = providers.Singleton(TextSegmenter)
    text_tokenizer = providers.Singleton(TextTokenizer)
    text_processor = providers.Singleton(TextProcessor)

    # Celery Tasks
    celery_cleanup_tasks = providers.Singleton(CleanupTasks)
    celery_download_tasks = providers.Singleton(DownloadTasks)
    celery_transcription_tasks = providers.Singleton(TranscriptionTasks)
    celery_shared_tasks = providers.Singleton(SharedTasks)

    # Dask Workers
    dask_text_processing_worker = providers.Singleton(TextProcessingWorker)
    dask_transcription_worker = providers.Singleton(TranscriptionWorker)
    dask_audio_conversion_worker = providers.Singleton(AudioConversionWorker)


# Initialize and Wire the Container
container = AppContainer()
container.wire(
    modules=[
        "src.app",
        "src.app.core",
        "src.app.infrastructure",
        "src.app.pipelines",
        "src.app.async_tasks",
        "src.app.cli",
    ]
)

# Log container initialization
logger = logging.getLogger(__name__)
logger.info("Dependency injection container successfully initialized and wired.")

# Exports for external modules
__all__ = ["container", "inject", "Provide"]
