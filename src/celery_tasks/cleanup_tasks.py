from celery import shared_task
from dependency_injector.wiring import inject, Provide
from src.infrastructure.dependency_setup import container  # This is used for wiring the dependencies.


@shared_task
@inject
def cleanup_old_data(
        logger=Provide[container.logger],
        file_manager=Provide[container.file_manager]
):
    """
    Celery task to clean up old data or files.
    """
    logger.info("Starting data cleanup task.")

    try:
        # Cleanup logic: Removing files older than a certain date
        directory_path = "/data/audio_files"
        retention_days = 30
        file_manager.remove_old_files(directory_path, days=retention_days)
        logger.info(f"Data cleanup completed for directory: {directory_path}, older than {retention_days} days.")
    except Exception as e:
        logger.error(f"Error during data cleanup: {e}")

    logger.info("Data cleanup task completed.")
