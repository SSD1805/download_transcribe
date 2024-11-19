import os
import yt_dlp
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker
from src.pipelines.registry.error_registry import DownloadError, ConfigurationError, FileError

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class DownloadManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = logger
        self.tracker = perf_tracker

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
        sanitized_name = "".join([c if c.isalnum() or c in " ._-()" else "_" for c in filename])
        self.logger.info(f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    def download(self, url):
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
                message = f"Unexpected error while downloading from {url}: {e}"
                self.logger.error(message)
                raise DownloadError(message) from e
