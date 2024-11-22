# src/infrastructure/dependency_setup.py

import logging

from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer

# Initialize the dependency injection container
container = AppContainer()

# Wire dependencies for the modules that actually require them
container.wire(
    modules=[
        # Core modules
        "src.app",
        "src.app.core.batch_processor",
        "src.app.core.memory_monitor",
        "src.app.core.services",
        # Infrastructure modules
        "src.app.infrastructure.registries.configuration_registry",
        "src.app.infrastructure.registries.model_registry",
        "src.app.infrastructure.registries.pipeline_registry",
        "src.app.infrastructure.registries.generic_registry",
        # Pipeline and module managers
        "src.app.modules.config_manager",
        "src.app.modules.pipeline_manager",
        "src.app.modules.transcription_manager",
        "src.app.modules.download_coordinator",
        "src.app.modules.audio_handler",
        "src.app.modules.helper_functions",
        "src.app.modules.text_handler",
        # Utility modules
        "src.app.utils.structlog_logger",
        "src.app.utils.tracking_utilities",
        "src.app.utils.file_utilities",
        "src.app.utils.concurrency_utilities",
        # CLI modules
        "src.app.cli.commands.base_command",
        "src.app.cli.cli_audio",
        "src.app.cli.cli_download",
        "src.app.cli.cli_text",
        "src.app.cli.cli_transcription",
        # Pipeline components that need injected services
        "src.app.pipelines.transcription.transcription_pipeline",
        "src.app.pipelines.transcription.audio_transcriber",
        "src.app.pipelines.transcription.transcription_saver",
        "src.app.pipelines.transcription.audio_processing_pipeline",
        "src.app.pipelines.download.youtube_downloader",
        "src.app.pipelines.download.download_handler",
        "src.app.pipelines.audio.audio_converter",
        "src.app.pipelines.text.text_loader",
        "src.app.pipelines.text.text_saver",
        "src.app.pipelines.text.ner_processor",
        "src.app.pipelines.text.text_segmenter",
        "src.app.pipelines.text.text_tokenizer",
        "src.app.pipelines.text.text_processor",
        # Celery tasks (only if they use dependency injection)
        "src.app.tasks.celery.cleanup_tasks",
        "src.app.tasks.celery.download_tasks",
        "src.app.tasks.celery.transcription_tasks",
        "src.app.tasks.celery.download_coordinator",
        "src.app.tasks.celery.shared_tasks",
        "src.app.tasks.celery.transcription_tasks",
        # Dependency injection for Dask tasks
        "src.app.tasks.dask.text_segmentation_worker",
        "src.app.tasks.dask.transcription_worker",
        "src.app.tasks.dask.text_tokenization_worker",
        "src.app.tasks.dask.text_loading_worker",
        "src.app.tasks.dask.text_saving_worker",
        "src.app.tasks.dask.pipeline_manager",
        "src.app.tasks.dask.performance_monitor_worker",
        "src.app.tasks.dask.ner_worker",
        "src.app.tasks.dask.audio_conversion_worker",
    ]
)

# Log successful container wiring
logger = logging.getLogger(__name__)
logger.info(
    "Dependency injection container has been successfully initialized and wired."
)

# Export container for use in other scripts
__all__ = ["container", "inject", "Provide"]

# Export Provide and inject for usage (optional aliases)
di_inject = inject
di_Provide = Provide
