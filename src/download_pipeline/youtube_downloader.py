from src.download_pipeline.download_manager import DownloadManager
from src.core.performance_tracker import PerformanceTracker
from src.core.logger_manager import LoggerManager

# Initialize logger
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()
download_manager = DownloadManager(logger=logger, tracker=perf_tracker)


class YouTubeDownloader:
    def __init__(self, download_manager, performance_tracker=None):
        """
        Initialize YouTubeDownloader with a DownloadManager and optionally a PerformanceTracker.
        """
        self.download_manager = download_manager
        self.performance_tracker = performance_tracker or PerformanceTracker()

    def download_video(self, url):
        """
        Download a single video with optional performance monitoring.
        """
        with self.performance_tracker.track_execution("download_video"):
            try:
                logger.info(f"Starting download for video: {url}")
                self.download_manager.download(url)
                logger.info(f"Video download completed: {url}")
            except Exception as e:
                logger.error(f"Failed to download video: {e}")

    def download_channel(self, channel_url):
        """
        Download an entire channel with optional performance monitoring.
        """
        with self.performance_tracker.track_execution("download_channel"):
            try:
                logger.info(f"Starting channel download from URL: {channel_url}")
                self.download_manager.download(channel_url)
                logger.info(f"Channel download completed from URL: {channel_url}")
            except Exception as e:
                logger.error(f"Failed to download channel: {e}")

    def download_playlist(self, playlist_url):
        """
        Download an entire playlist with optional performance monitoring.
        """
        with self.performance_tracker.track_execution("download_playlist"):
            try:
                logger.info(f"Starting playlist download from URL: {playlist_url}")
                self.download_manager.download(playlist_url)
                logger.info(f"Playlist download completed from URL: {playlist_url}")
            except Exception as e:
                logger.error(f"Failed to download playlist: {e}")

    def download_batch(self, urls, batch_size=3):
        """
        Download videos in batches using PerformanceTracker.
        """
        def download_single_url(url):
            self.download_video(url)

        logger.info("Starting batch download...")
        self.performance_tracker.batch_process(download_single_url, urls, batch_size=batch_size)
        logger.info("Batch download completed.")
