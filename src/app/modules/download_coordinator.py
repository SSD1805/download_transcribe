from abc import ABC, abstractmethod
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer


# Base Command Class
class DownloadCommand(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass


# Concrete Commands
class DownloadVideoCommand(DownloadCommand):
    @inject
    def __init__(
        self,
        download_manager=Provide[
            AppContainer.pipeline_component_registry.provide("download_manager")
        ],
        logger=Provide[AppContainer.logger],
    ):
        self.download_manager = download_manager
        self.logger = logger

    def execute(self, **kwargs):
        video_url = kwargs.get("video_url")
        output_directory = kwargs.get("output_directory")

        try:
            self.logger.info(
                f"Downloading video from {video_url} to {output_directory}"
            )
            self.download_manager.download_video(video_url, output_directory)
            self.logger.info(
                f"Successfully downloaded video from {video_url} to {output_directory}"
            )
        except Exception as e:
            self.logger.error(f"Failed to download video from {video_url}: {e}")
            raise


class DownloadChannelCommand(DownloadCommand):
    @inject
    def __init__(
        self,
        download_manager=Provide[
            AppContainer.pipeline_component_registry.provide("download_manager")
        ],
        logger=Provide[AppContainer.logger],
    ):
        self.download_manager = download_manager
        self.logger = logger

    def execute(self, **kwargs):
        channel_url = kwargs.get("channel_url")
        output_directory = kwargs.get("output_directory")

        try:
            self.logger.info(
                f"Downloading all videos from channel {channel_url} to {output_directory}"
            )
            self.download_manager.download_channel(channel_url, output_directory)
            self.logger.info(
                f"Successfully downloaded all videos from channel {channel_url} to {output_directory}"
            )
        except Exception as e:
            self.logger.error(f"Failed to download channel from {channel_url}: {e}")
            raise


class DownloadPlaylistCommand(DownloadCommand):
    @inject
    def __init__(
        self,
        download_manager=Provide[
            AppContainer.pipeline_component_registry.provide("download_manager")
        ],
        logger=Provide[AppContainer.logger],
    ):
        self.download_manager = download_manager
        self.logger = logger

    def execute(self, **kwargs):
        playlist_url = kwargs.get("playlist_url")
        output_directory = kwargs.get("output_directory")

        try:
            self.logger.info(
                f"Downloading all videos from playlist {playlist_url} to {output_directory}"
            )
            self.download_manager.download_playlist(playlist_url, output_directory)
            self.logger.info(
                f"Successfully downloaded all videos from playlist {playlist_url} to {output_directory}"
            )
        except Exception as e:
            self.logger.error(f"Failed to download playlist from {playlist_url}: {e}")
            raise
