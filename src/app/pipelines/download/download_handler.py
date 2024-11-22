import os

import yt_dlp
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class DownloadManager:
    @inject
    def __init__(
        self,
        config_manager=Provide[AppContainer.configuration_registry],
        logger=Provide[AppContainer.logger],
        perf_tracker=Provide[AppContainer.performance_tracker],
        error_registry=Provide[AppContainer.error_registry],
    ):
        """
        Initialize the DownloadManager.

        Args:
            config_manager: The configuration registry to fetch configurations.
            logger: Logger instance for logging activities.
            perf_tracker: Performance tracker for measuring execution times.
            error_registry: Error registry for custom exceptions like DownloadError, ConfigurationError, FileError.
        """
        self.config_manager = config_manager
        self.logger = logger
        self.tracker = perf_tracker
        self.error_registry = error_registry

        try:
            self.download_directory = self.config_manager.get(
                "download_directory", "/data/audio_files"
            )
            self.yt_dlp_options = self.config_manager.get(
                "yt_dlp_options",
                {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(
                        self.download_directory, "%(title)s.%(ext)s"
                    ),
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                },
            )
            if not os.path.exists(self.download_directory):
                raise self.error_registry.FileError(
                    f"Download directory does not exist: {self.download_directory}"
                )
            self.logger.info(
                f"DownloadManager initialized with directory: {self.download_directory}"
            )
        except KeyError as e:
            message = f"Missing configuration key: {e}"
            self.logger.error(message)
            raise self.error_registry.ConfigurationError(message) from e
        except self.error_registry.FileError as e:
            self.logger.error(str(e))
            raise

    def sanitize_filename(self, filename):
        sanitized_name = "".join(
            [c if c.isalnum() or c in " ._-()" else "_" for c in filename]
        )
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
                raise self.error_registry.DownloadError(message) from e
            except Exception as e:
                message = f"Unexpected error while downloading from {url}: {e}"
                self.logger.error(message)
                raise self.error_registry.DownloadError(message) from e
