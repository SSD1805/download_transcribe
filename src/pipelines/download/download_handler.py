import os

import yt_dlp

from src.core.services import CoreServices
from src.pipelines.registry.error_registry import DownloadError, ConfigurationError, FileError

# Get logger and performance tracker from CoreServices
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


class DownloadManager:
    def __init__(self, config_manager, logger=None, tracker=None):
        """
        Initialize the DownloadManager with a specified configuration manager, logger,
        and performance tracker for flexible injection and centralized configuration.

        Args:
            config_manager (ConfigManager): Instance of ConfigManager to manage configurations.
            logger (Logger, optional): Logger instance for logging messages. Defaults to None.
            tracker (PerformanceTracker, optional): Instance of PerformanceTracker
                for performance tracking. Defaults to None.
        """
        self.config_manager = config_manager
        self.logger = logger or LoggerManager().get_logger()
        self.tracker = tracker or PerformanceTracker()

        # Attempt to load configuration values
        try:
            self.download_directory = self.config_manager.get('download_directory', '/data/audio_files')
            self.yt_dlp_options = self.config_manager.get('yt_dlp_options', {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_directory, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
            if not os.path.exists(self.download_directory):
                raise FileError(f"Download directory does not exist: {self.download_directory}")
            self.logger.info(f"DownloadManager initialized with directory: {self.download_directory}")

        except KeyError as e:
            message = f"Missing configuration key: {e}"
            self.logger.error(message)
            raise ConfigurationError(message) from e
        except FileError as e:
            self.logger.error(str(e))
            raise

    def sanitize_filename(self, filename):
        """
        Sanitize filenames to ensure they are safe for file systems.

        Args:
            filename (str): The filename to sanitize.

        Returns:
            str: A sanitized version of the filename.
        """
        sanitized_name = "".join([c if c.isalnum() or c in " ._-()" else "_" for c in filename])
        self.logger.info(f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    def download(self, url):
        """
        Download a single video from a URL with performance tracking.

        Args:
            url (str): The URL of the video to download.

        Raises:
            DownloadError: If the download fails, an exception is raised with an error message.
        """
        with self.tracker.track_execution("Video Download"):
            try:
                with yt_dlp.YoutubeDL(self.yt_dlp_options) as ydl:
                    self.logger.info(f"Starting download from URL: {url}")
                    ydl.download([url])
                    self.logger.info(f"Download completed for URL: {url}")
            except yt_dlp.DownloadError as e:
                message = f"Error during download from {url}: {e}"
                self.logger.error(message)
                raise DownloadError(message) from e
            except Exception as e:
                # Capture any other unexpected errors
                message = f"Unexpected error while downloading from {url}: {e}"
                self.logger.error(message)
                raise DownloadError(message) from e
