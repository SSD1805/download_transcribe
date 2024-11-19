from src.infrastructure.app_container import containers, providers
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker
from src.modules.config_manager import ConfigManager
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


class AppContainer(containers.DeclarativeContainer):
    """Unified Dependency Injection Container for the Application"""

    # Configuration
    config = providers.Singleton(ConfigManager, config_path="config.yaml")

    # Shared Utilities
    logger = providers.Singleton(StructLogger.get_logger)
    performance_tracker = providers.Singleton(PerformanceTracker.get_instance)

    # Registries
    config_registry = providers.Singleton(ConfigurationRegistry)
    error_registry = providers.Singleton(ErrorRegistry)
    model_registry = providers.Singleton(ModelRegistry)
    pipeline_component_registry = providers.Singleton(PipelineComponentRegistry)

    # Provide Pipeline Components
    @pipeline_component_registry.provider
    def provide_pipeline_components(self):
        registry = PipelineComponentRegistry()

        # Transcription Components
        registry.register("transcription_pipeline", TranscriptionPipeline)
        registry.register("transcription_saver", TranscriptionSaver)

        # Audio Processing Components
        registry.register("audio_handler", AudioHandler)

        # Downloading Components
        registry.register("download_manager", DownloadManager, config_manager=self.config())
        registry.register(
            "youtube_downloader",
            YouTubeDownloader,
            download_manager=registry.get("download_manager"),
        )

        # Text Processing Components
        registry.register("ner_processor", NERProcessor)
        registry.register("text_loader", TextLoader)
        registry.register("text_saver", TextSaver)
        registry.register("text_segmenter", TextSegmenter)
        registry.register("text_tokenizer", TextTokenizer)

        return registry

    # Transcriber Service
    transcriber = providers.Factory(AudioTranscriber)
