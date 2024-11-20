from celery_app import shared_task
from dependency_injector.wiring import inject, Provide
from infrastructure.dependency_setup import container

@shared_task(bind=True, max_retries=3)
@inject
def download_video_task(self,
                        url: str,
                        download_manager=Provide[container.download_manager],
                        logger=Provide[container.logger]):
    """
    Celery task to download a video using DownloadManager.

    Args:
        self:
        url (str): The video URL to download.
        download_manager: Injected DownloadManager instance for handling video downloads.
        logger: Injected Logger instance for logging information.

    Raises:
        Exception: If the download fails after retries.
    """
    try:
        logger.info(f"Starting download task for URL: {url}")
        result = download_manager.download(url)
        logger.info(f"Download completed for URL: {url}")
        return result
    except Exception as e:
        logger.error(f"Download failed for URL: {url} with error: {e}")
        raise self.retry(countdown=60, exc=e)
