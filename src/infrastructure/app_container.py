from dependency_injector import containers, providers
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker
from src.utils.concurrency_manager import ConcurrencyManager
from src.utils.file_utilities import FileManager, DirectoryManager, FilenameSanitizer
from src.utils.progress_bar import ProgressBar
from src.utils.timestamp_formatter import TimestampFormatter
from src.utils.yaml_parser import YAMLParser
from src.pipelines.transcription.audio_transcriber import AudioTranscriber
from src.pipelines.transcription.transcription_pipeline import TranscriptionPipeline
from src.pipelines.transcription.transcription_saver import TranscriptionSaver
from src.pipelines.audio.audio_handler import AudioHandler
from src.pipelines.download.download_handler import DownloadManager
from src.pipelines.download.youtube_downloader import YouTubeDownloader
from src.pipelines.text.ner_processor import NERProcessor
from src.pipelines.text.text_loader import TextLoader
from src.pipelines.text.text_saver import TextSaver
from src.pipelines.text.text_segmenter import TextSegmenter
from src.pipelines.text.text_tokenizer import TextTokenizer
from src.infrastructure.registries.configuration_registry import ConfigurationRegistry
from src.infrastructure.registries.error_registry import ErrorRegistry
from src.infrastructure.registries.model_registry import ModelRegistry
from src.infrastructure.registries.pipeline_component_registry import PipelineComponentRegistry
from src.core.batch_processor import BatchProcessor
from src.core.memory_monitor import MemoryMonitor
from src.core.services import SingletonLogger, SingletonPerformanceTracker
from src.modules.audio_handler import AudioHandler
from src.modules.download_coordinator import DownloadCoordinator
from src.modules.pipeline_manager import PipelineManager
from src.modules.text_processor import TextProcessor
from src.modules.transcription_manager import ModelLoader
from src.modules.helper_functions import HelperFunctions
import structlog
import logging
import os

class AppContainer(containers.DeclarativeContainer):
    """Unified Dependency Injection Container for the Application"""

    # Centralized Configuration Registry
    configuration_registry = providers.Singleton(ConfigurationRegistry)

    # Shared Utilities
    logger = providers.Singleton(SingletonLogger.get_instance)
    performance_tracker = providers.Singleton(SingletonPerformanceTracker.get_instance)
    error_registry = providers.Singleton(ErrorRegistry)
    memory_monitor = providers.Singleton(
        MemoryMonitor, threshold=configuration_registry().get('memory', {}).get('threshold', 80)
    )  # Threshold set via configuration
    helper_functions = providers.Singleton(HelperFunctions)
    concurrency_manager = providers.Singleton(ConcurrencyManager)
    file_manager = providers.Singleton(FileManager)
    directory_manager = providers.Singleton(DirectoryManager)
    filename_sanitizer = providers.Singleton(FilenameSanitizer)
    progress_bar = providers.Singleton(ProgressBar)
    timestamp_formatter = providers.Singleton(TimestampFormatter)
    yaml_parser = providers.Singleton(YAMLParser)

    # Structlog Configuration
    @staticmethod
    def configure_structlog():
        """Configure Structlog based on environment settings"""
        environment = AppContainer.configuration_registry().get("environment", "development")
        renderer = structlog.processors.JSONRenderer() if environment != "development" else structlog.dev.ConsoleRenderer()

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                StructLogger.add_custom_context,  # Custom processor for additional context
                renderer
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    configure_structlog()

    # Configure stdlib logger to integrate with structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=configuration_registry().get("logging", {}).get("level", "INFO"),
    )

    # Adding File Handler for persistent logs
    file_handler = logging.FileHandler(configuration_registry().get("logging", {}).get("file_path", "app.log"))
    file_handler.setLevel(logging.INFO)
    logger_instance = logging.getLogger("custom_logger")
    logger_instance.addHandler(file_handler)

    # Registries
    model_registry = providers.Singleton(ModelRegistry)
    pipeline_component_registry = providers.Singleton(PipelineComponentRegistry)

    # Provide Pipeline Components
    @pipeline_component_registry.provider
    def provide_pipeline_components(self):
        registry = PipelineComponentRegistry()

        # Transcription Components
        registry.register("transcription_pipeline", TranscriptionPipeline)
        registry.register("transcription_saver", TranscriptionSaver)
        registry.register("model_loader", ModelLoader)

        # Audio Processing Components
        registry.register("audio_handler", AudioHandler)

        # Downloading Components
        registry.register("download_manager", DownloadManager, config_manager=self.configuration_registry())
        registry.register(
            "youtube_downloader",
            YouTubeDownloader,
            download_manager=registry.get("download_manager"),
        )
        registry.register("download_coordinator", DownloadCoordinator)

        # Text Processing Components
        registry.register("ner_processor", NERProcessor)
        registry.register("text_loader", TextLoader)
        registry.register("text_saver", TextSaver)
        registry.register("text_segmenter", TextSegmenter)
        registry.register("text_tokenizer", TextTokenizer)
        registry.register("text_processor", TextProcessor)

        return registry

    # Transcriber Service
    transcriber = providers.Factory(AudioTranscriber)

    # Batch Processor
    batch_processor = providers.Factory(
        BatchProcessor, logger=logger, performance_tracker=performance_tracker
    )

    # Pipeline Manager
    pipeline_manager = providers.Factory(
        PipelineManager, batch_processor=batch_processor, memory_monitor=memory_monitor, logger=logger, concurrency_manager=concurrency_manager
    )

    # Register Celery Tasks
    @staticmethod
    def register_celery_tasks():
        """Dynamically register Celery tasks"""
        task_names = ["cleanup_tasks", "download_tasks", "transcription_tasks", "shared_tasks"]
        for task_name in task_names:
            setattr(AppContainer, f"{task_name}", providers.Factory(f'src.celery_tasks.{task_name}'))

    register_celery_tasks()
