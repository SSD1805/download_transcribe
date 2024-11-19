from celery import shared_task
from src.pipelines.download.download_handler import DownloadManager
from src.pipelines.registry.error_registry import DownloadError
from src.utils.structlog_logger import StructLogger

logger = StructLogger.get_logger()

@shared_task(bind=True, max_retries=3)
def download_video_task(self, url, config_manager):
    """
    Celery task to download a video using DownloadManager.

    Args:
        url (str): The video URL to download.
        config_manager (ConfigManager): Configuration manager.

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
        self.retry(countdown=60, exc=e)
