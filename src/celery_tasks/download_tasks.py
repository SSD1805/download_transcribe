# celery_tasks/download_tasks.py

from celery import shared_task
from src.core.logger_manager import LoggerManager
from src.download_pipeline.download_manager import DownloadManager  # Ensure the path aligns with your project structure
from src.download_pipeline.custom_exceptions import DownloadError

logger = LoggerManager().get_logger()

@shared_task(bind=True, max_retries=3)
def download_video_task(self, url, config_manager):
    """
    Celery task to download a video using DownloadManager.

    Args:
        url (str): The video URL to download.
        config_manager (ConfigManager): Configuration manager for centralized settings.

    Raises:
        DownloadError: If the download fails after retries.
    """
    try:
        logger.info(f"Starting download task for URL: {url}")
        download_manager = DownloadManager(config_manager)
        result = download_manager.download(url)
        logger.info(f"Download completed for URL: {url}")
        return result
    except DownloadError as e:
        logger.error(f"Download failed for URL: {url} with error: {e}")
        self.retry(countdown=60, exc=e)  # Retry in 60 seconds if it fails
