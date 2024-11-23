import structlog
from dependency_injector import containers, providers

from src.app.cli import (
    BatchDownloadCommand,
    ConvertAudioCommand,
    DownloadChannelCommand,
    DownloadPlaylistCommand,
    DownloadVideoCommand,
    LoadTextCommand,
    NormalizeAudioCommand,
    ProcessTextCommand,
    SaveTextCommand,
    SaveTranscriptionCommand,
    SplitAudioCommand,
    TranscribeCommand,
    TrimAudioCommand,
)
from src.app.core import SingletonLogger, SingletonPerformanceTracker
from src.app.modules import HelperFunctions, PipelineManager
from src.app.pipelines.audio_processing import (
    AudioConverter,
    AudioNormalizer,
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
from src.app.utils import ConcurrentTask, FileUtilityFacade, StructLogger
from src.infrastructure.registries import (
    ConfigurationRegistry,
    ModelRegistry,
    PipelineRegistry,
)


class AppContainer(containers.DeclarativeContainer):
    """Unified Dependency Injection Container for the Application"""

    # Configuration Registry
    configuration_registry = providers.Singleton(ConfigurationRegistry)

    # Shared Utilities
    logger = providers.Singleton(SingletonLogger.get_instance)
    performance_tracker = providers.Singleton(SingletonPerformanceTracker.get_instance)
    concurrent_task = providers.Singleton(ConcurrentTask)
    file_utilities = providers.Singleton(FileUtilityFacade)
    timestamp = providers.Singleton(HelperFunctions.get_timestamp)

    # Structlog Configuration
    @providers.Singleton
    def configure_structlog() -> None:
        """Configure Structlog based on environment settings"""
        environment = configuration_registry().get("environment", "development")
        renderer = (
            structlog.processors.JSONRenderer()
            if environment != "development"
            else structlog.dev.ConsoleRenderer()
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                StructLogger.add_custom_context,
                renderer,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    # Text Processing Components
    text_loader = providers.Singleton(TextLoader)
    text_segmenter = providers.Singleton(TextSegmenter)
    text_tokenizer = providers.Singleton(TextTokenizer)
    text_saver = providers.Singleton(TextSaver)

    # Audio Pipeline Components
    audio_converter = providers.Singleton(AudioConverter)
    audio_splitter = providers.Singleton(AudioSplitter)
    audio_normalizer = providers.Singleton(AudioNormalizer)
    audio_trimmer = providers.Singleton(AudioTrimmer)

    # Transcription Pipeline Components
    transcriber = providers.Singleton(AudioTranscriber)
    transcription_pipeline = providers.Singleton(TranscriptionPipeline)

    # CLI Commands
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
    text_commands = providers.Factory(
        load_command=LoadTextCommand,
        process_command=ProcessTextCommand,
        save_command=SaveTextCommand,
    )
    transcription_commands = providers.Factory(
        TranscribeCommand, save_command=SaveTranscriptionCommand
    )

    # Registries
    model_registry = providers.Singleton(ModelRegistry)
    pipeline_registry = providers.Singleton(PipelineRegistry)

    # Pipeline Manager
    pipeline_manager = providers.Singleton(
        PipelineManager,
        batch_processor=providers.Singleton(
            BatchProcessor, logger=logger, performance_tracker=performance_tracker
        ),
        memory_monitor=providers.Singleton(
            MemoryMonitor,
            threshold=configuration_registry().get("memory", {}).get("threshold", 80),
        ),
        logger=logger,
        concurrency_manager=concurrent_task,
    )

    # Dynamic Pipeline Registration
    @pipeline_registry.provider
    def provide_pipeline_components() -> PipelineRegistry:
        """Dynamically register pipeline components"""
        registry = PipelineRegistry()

        # Transcription Components
        registry.register("transcription_pipeline", TranscriptionPipeline)
        registry.register("audio_transcriber", AudioTranscriber)

        # Audio Components
        registry.register("audio_converter", AudioConverter)
        registry.register("audio_splitter", AudioSplitter)
        registry.register("audio_normalizer", AudioNormalizer)
        registry.register("audio_trimmer", AudioTrimmer)

        # Text Components
        registry.register("text_loader", TextLoader)
        registry.register("text_segmenter", TextSegmenter)
        registry.register("text_tokenizer", TextTokenizer)
        registry.register("text_saver", TextSaver)

        return registry
