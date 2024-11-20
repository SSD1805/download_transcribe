# src/infrastructure/dependency_setup.py

from src.infrastructure.app_container import AppContainer
from dependency_injector.wiring import Provide, inject
import logging

# Initialize the dependency injection container
container = AppContainer()

# Wire dependencies for the modules that actually require them
container.wire(modules=[
    # Core modules
    "src.app",
    "src.core.batch_processor",
    "src.core.memory_monitor",
    "src.core.services",

    # Infrastructure modules
    "src.infrastructure.registries.configuration_registry",
    "src.infrastructure.registries.error_registry",
    "src.infrastructure.registries.model_registry",
    "src.infrastructure.registries.pipeline_component_registry",

    # Pipeline and module managers
    "src.modules.config_manager",
    "src.modules.pipeline_manager",
    "src.modules.transcription_manager",
    "src.modules.download_coordinator",
    "src.modules.audio_handler",
    "src.modules.helper_functions",
    "src.modules.text_processor",


    # CLI modules
    "src.cli.cli_audio",
    "src.cli.cli_download",
    "src.cli.cli_text",
    "src.cli.cli_transcription",

    # Pipeline components that need injected services
    "src.pipelines.transcription.transcription_pipeline",
    "src.pipelines.audio.audio_handler",
    "src.pipelines.download.download_handler",
    "src.pipelines.text.text_loader",
    "src.pipelines.text.text_saver",
    "src.pipelines.text.ner_processor",

    # Celery tasks (only if they use dependency injection)
    "src.celery_tasks.cleanup_tasks",
    "src.celery_tasks.download_tasks",
    "src.celery_tasks.transcription_tasks",
    "src.celery_tasks.download_coordinator",
    "src.celery_tasks.shared_tasks"
    "src.celery_tasks.transcription_tasks"
])

# Log successful container wiring
logger = logging.getLogger(__name__)
logger.info("Dependency injection container has been successfully initialized and wired.")

# Export container for use in other scripts
__all__ = ["container", "inject", "Provide"]

# Export Provide and inject for usage (optional aliases)
di_inject = inject
di_Provide = Provide
