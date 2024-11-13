import os
import yt_dlp
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceManager

# Initialize logger and performance manager
log_manager = LoggerManager()
logger = log_manager.get_logger()
perf_manager = PerformanceManager()

class DownloadManager:
    def __init__(self, download_directory='app/audio_files', yt_dlp_options=None):
        """
        Initialize the DownloadManager with the specified download directory and yt-dlp options.
        """
        self.download_directory = download_directory
        self.yt_dlp_options = yt_dlp_options or {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_directory, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        logger.info(f"DownloadManager initialized with directory: {self.download_directory}")

    def sanitize_filename(self, filename):
        """
        Sanitize filenames to ensure they are safe for file systems.
        """
        return "".join([c if c.isalnum() or c in " ._-()" else "_" for c in filename])

    @perf_manager.track_performance  # Add the performance tracker decorator
    def download(self, url):
        """
        Download a single video from a URL with performance tracking.
        """
        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as ydl:
                logger.info(f"Downloading from URL: {url}")
                ydl.download([url])
                logger.info(f"Download completed for URL: {url}")
        except Exception as e:
            logger.error(f"Error downloading from {url}: {e}")
            raise
