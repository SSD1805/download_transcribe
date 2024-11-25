from celery import Celery
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app.app_container import AppContainer
from src.infrastructure.app.configuration_registry import ConfigurationRegistry


@inject
def create_celery_app(
        config_registry: ConfigurationRegistry = Provide[AppContainer.configuration_registry],
        logger=Provide[AppContainer.logger],
) -> Celery:
    """
    Create and configure a Celery app instance using ConfigurationRegistry.

    Args:
        config_registry (ConfigurationRegistry): The configuration registry for app settings.
        logger: Logger instance for observability.

    Returns:
        Celery: Configured Celery app instance.
    """
    logger.info("Initializing Celery app...")

    # Retrieve Celery-specific configurations from the registry
    broker_url = config_registry.get("celery_broker_url")
    result_backend = config_registry.get("celery_result_backend")
    task_serializer = config_registry.get("celery_task_serializer")
    accept_content = config_registry.get("celery_accept_content")
    result_serializer = config_registry.get("celery_result_serializer")
    timezone = config_registry.get("celery_timezone")
    enable_utc = config_registry.get("celery_enable_utc")
    task_track_started = config_registry.get("celery_task_track_started")
    task_time_limit = config_registry.get("celery_task_time_limit")

    # Initialize the Celery app
    celery_app = Celery(
        "transcription_pipeline",
        broker=broker_url,
        backend=result_backend,
    )

    # Update Celery configurations
    celery_app.conf.update(
        task_serializer=task_serializer,
        accept_content=accept_content,
        result_serializer=result_serializer,
        timezone=timezone,
        enable_utc=enable_utc,
        task_track_started=task_track_started,
        task_time_limit=task_time_limit,
    )

    logger.info("Celery app initialized and configured.")
    return celery_app


# Create and expose the Celery app instance
celery_app = create_celery_app()
