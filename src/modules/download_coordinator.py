from abc import ABC, abstractmethod
from src.utils.logger_service import LoggerService

from src.pipelines.registry.preconfigured_audio_handler_registry import PreConfiguredAudioHandlerRegistry


# Base Command Class
class DownloadCommand(ABC):
    """
    Abstract base class representing a download command.
    """
    @abstractmethod
    def execute(self, **kwargs):
        pass

# Concrete Commands
class DownloadVideoCommand(DownloadCommand):
    def execute(self, **kwargs):
        video_url = kwargs.get('video_url')
        output_directory = kwargs.get('output_directory')
        logger = LoggerService.get_instance()
        logger.info(f"Downloading video from {video_url} to {output_directory}")
        # Implement video download logic here

class DownloadChannelCommand(DownloadCommand):
    def execute(self, **kwargs):
        channel_url = kwargs.get('channel_url')
        output_directory = kwargs.get('output_directory')
        logger = LoggerService.get_instance()
        logger.info(f"Downloading all videos from channel {channel_url} to {output_directory}")
        # Implement channel download logic here

class DownloadPlaylistCommand(DownloadCommand):
    def execute(self, **kwargs):
        playlist_url = kwargs.get('playlist_url')
        output_directory = kwargs.get('output_directory')
        logger = LoggerService.get_instance()
        logger.info(f"Downloading all videos from playlist {playlist_url} to {output_directory}")
        # Implement playlist download logic here

# Handler Class
class DownloadHandler:
    """
    Download handler that uses a registry to retrieve and execute download commands.
    """
    def __init__(self, handler_registry):
        self.handler_registry = handler_registry
        self.logger = LoggerService.get_instance()

    def handle_download(self, operation_name: str, **kwargs):
        """
        Handle a download operation by delegating to the appropriate command.

        Args:
            operation_name (str): The operation to perform (e.g., 'download_video', 'download_channel').
            **kwargs: Arguments required by the command.
        """
        try:
            command = self.handler_registry.get(operation_name)
            self.logger.info(f"Executing download operation '{operation_name}'")
            command.execute(**kwargs)
        except ValueError as e:
            self.logger.error(f"Command for operation '{operation_name}' not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to execute command for operation '{operation_name}': {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Assuming handler_registry is already configured with commands
    handler_registry = PreConfiguredAudioHandlerRegistry()  # Should be a Download-specific registry in practice
    handler_registry.register("download_video", DownloadVideoCommand())
    handler_registry.register("download_channel", DownloadChannelCommand())
    handler_registry.register("download_playlist", DownloadPlaylistCommand())

    download_handler = DownloadHandler(handler_registry)

    # Download video
    download_handler.handle_download("download_video", video_url="https://youtube.com/watch?v=example_video_id", output_directory="/downloads")

    # Download channel
    download_handler.handle_download("download_channel", channel_url="https://youtube.com/channel/example_channel_id", output_directory="/downloads")

    # Download playlist
    download_handler.handle_download("download_playlist", playlist_url="https://youtube.com/playlist?list=example_playlist_id", output_directory="/downloads")
