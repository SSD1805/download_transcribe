from src.download_pipeline.download_manager import DownloadManager
from src.core.performance_tracker import PerformanceTracker
from src.core.logger_manager import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

class YouTubeDownloader:
    def __init__(self, download_manager, performance_tracker=None):
        """
        Initialize YouTubeDownloader with a DownloadManager and optionally a PerformanceTracker.
        """
        self.download_manager = download_manager
        self.performance_manager = performance_tracker or PerformanceTracker()

    def download_video(self, url):
        """
        Download a single video with optional performance monitoring.
        """
        if self.performance_manager:
            self.performance_manager.monitor_memory_usage()
        try:
            self.download_manager.download(url)
        except Exception as e:
            logger.error(f"Failed to download video: {e}")

    def download_channel(self, channel_url):
        """
        Download an entire channel with optional performance monitoring.
        """
        if self.performance_manager:
            self.performance_manager.monitor_memory_usage()
        try:
            logger.info(f"Starting channel download from URL: {channel_url}")
            self.download_manager.download(channel_url)
        except Exception as e:
            logger.error(f"Failed to download channel: {e}")

    def download_playlist(self, playlist_url):
        """
        Download an entire playlist with optional performance monitoring.
        """
        if self.performance_manager:
            self.performance_manager.monitor_memory_usage()
        try:
            logger.info(f"Starting playlist download from URL: {playlist_url}")
            self.download_manager.download(playlist_url)
        except Exception as e:
            logger.error(f"Failed to download playlist: {e}")

    def download_batch(self, urls, batch_size=3):
        """
        Download videos in batches using PerformanceTracker.
        """
        def download_single_url(url):
            self.download_video(url)

        if self.performance_manager:
            logger.info("Starting batch download...")
            self.performance_manager.batch_process(download_single_url, urls, batch_size=batch_size)
            logger.info("Batch download completed.")