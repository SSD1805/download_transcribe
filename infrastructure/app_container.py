from dependency_injector import containers, providers
from src.utils.structlog_logger import StructLogger
from src.utils.concurrency_utilities import ConcurrencyManager
from src.utils.file_utilities import FileManager, DirectoryManager, FilenameSanitizer
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
from infrastructure.registries.configuration_registry import ConfigurationRegistry
from infrastructure.registries.model_registry import ModelRegistry
from infrastructure.registries.pipeline_registry import PipelineRegistry
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
from tasks.observers import LoggerObserver


class AppContainer(containers.DeclarativeContainer):
    """Unified Dependency Injection Container for the Application"""

    # Centralized Configuration Registry
    configuration_registry = providers.Singleton(ConfigurationRegistry)

    # Shared Utilities
    logger = providers.Singleton(SingletonLogger.get_instance)
    performance_tracker = providers.Singleton(SingletonPerformanceTracker.get_instance)
    error_registry = providers.Singleton(ErrorRegistry, logger=logger)
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
    @providers.Singleton
    @performance_tracker().track
    def configure_structlog(self) -> None:
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

    # Configure stdlib logger to integrate with structlog
    @providers.Singleton
    @performance_tracker().track
    def configure_stdlib_logger(self) -> None:
        logging.basicConfig(
            format="%(message)s",
            level=AppContainer.configuration_registry().get("logging", {}).get("level", "INFO"),
        )
        file_handler = logging.FileHandler(AppContainer.configuration_registry().get("logging", {}).get("file_path", "app.log"))
        file_handler.setLevel(logging.INFO)
        custom_logger = logging.getLogger("custom_logger")
        custom_logger.addHandler(file_handler)

    # Registries
    model_registry = providers.Singleton(ModelRegistry)
    pipeline_component_registry = providers.Singleton(PipelineComponentRegistry)

    # Provide Pipeline Components
    @pipeline_component_registry.provider
    @performance_tracker().track
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
    def register_celery_tasks(self):
        """Register Celery tasks dynamically"""
        task_mapping = {
            "cleanup_tasks": "src.celery.cleanup_tasks.cleanup_old_data",
            "download_tasks": "src.celery.download_tasks.download_video_task",
            "transcription_tasks": "src.celery.transcription_tasks.transcribe_audio_task",
            "shared_tasks": "src.celery.shared_tasks.update_task_status",
        }

        for name, task_path in task_mapping.items():
            setattr(self, name, providers.Factory(task_path, logger=self.logger, progress_bar=self.progress_bar))

    register_celery_tasks()  # Register Celery tasks
