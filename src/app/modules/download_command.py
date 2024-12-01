from abc import ABC, abstractmethod

from dependency_injector.wiring import inject

from src.infrastructure.app.app_container import AppContainer


# Base Command Class
class DownloadCommand(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass


# Concrete Commands
@inject
class DownloadVideoCommand(DownloadCommand):
    def __init__(
        self,
        download_manager=None,
        logger=None,
    ):
        self.download_manager = (
            download_manager or AppContainer.pipeline_component_registry.provide("download_manager")
        )
        self.logger = logger or AppContainer.logger

    def execute(self, **kwargs):
        video_url = kwargs.get("video_url")
        output_directory = kwargs.get("output_directory")

        try:
            self.logger.info(
                f"Downloading video from {video_url} to {output_directory}"
            )
            self.download_manager.download_video(video_url, output_directory)
            self.logger.info(
                f"Successfully downloaded video from {video_url} "
                f"to {output_directory}"
            )
        except Exception as e:
            self.logger.error(f"Failed to download video from {video_url}: {e}")
            raise


@inject
class DownloadChannelCommand(DownloadCommand):
    def __init__(
        self,
        download_manager=None,
        logger=None,
    ):
        self.download_manager = (
            download_manager or AppContainer.pipeline_component_registry.provide("download_manager")
        )
        self.logger = logger or AppContainer.logger

    def execute(self, **kwargs):
        channel_url = kwargs.get("channel_url")
        output_directory = kwargs.get("output_directory")

        try:
            self.logger.info(
                f"Downloading all videos from channel {channel_url} "
                f"to {output_directory}"
            )
            self.download_manager.download_channel(channel_url, output_directory)
            self.logger.info(
                f"Successfully downloaded all videos from channel {channel_url} "
                f"to {output_directory}"
            )
        except Exception as e:
            self.logger.error(f"Failed to download channel from {channel_url}: {e}")
            raise


@inject
class DownloadPlaylistCommand(DownloadCommand):
    def __init__(
        self,
        download_manager=None,
        logger=None,
    ):
        self.download_manager = (
            download_manager or AppContainer.pipeline_component_registry.provide("download_manager")
        )
        self.logger = logger or AppContainer.logger

    def execute(self, **kwargs):
        playlist_url = kwargs.get("playlist_url")
        output_directory = kwargs.get("output_directory")

        try:
            self.logger.info(
                f"Downloading all videos from playlist {playlist_url} "
                f"to {output_directory}"
            )
            self.download_manager.download_playlist(playlist_url, output_directory)
            self.logger.info(
                f"Successfully downloaded all videos from playlist {playlist_url} "
                f"to {output_directory}"
            )
        except Exception as e:
            self.logger.error(f"Failed to download playlist from {playlist_url}: {e}")
            raise
