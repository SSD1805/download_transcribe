from celery import shared_task
from src.utils.structlog_logger import StructLogger

logger = StructLogger.get_logger()

@shared_task
def cleanup_old_data():
    """
    Celery task to clean up old data or files.
    """
    logger.info("Starting data cleanup task.")
    # Implement cleanup logic here
    # Example: Removing files older than a certain date
    # file_manager = FileManager()
    # file_manager.remove_old_files('/data/audio_files', days=30)
    logger.info("Data cleanup task completed.")
