from abc import ABC, abstractmethod
from src.utils.structlog_logger import StructLogger

logger = StructLogger.get_logger()

# Base Command Class
class DownloadCommand(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

# Concrete Commands
class DownloadVideoCommand(DownloadCommand):
    def execute(self, **kwargs):
        video_url = kwargs.get('video_url')
        output_directory = kwargs.get('output_directory')
        logger.info(f"Downloading video from {video_url} to {output_directory}")
        # Implement video download logic here

class DownloadChannelCommand(DownloadCommand):
    def execute(self, **kwargs):
        channel_url = kwargs.get('channel_url')
        output_directory = kwargs.get('output_directory')
        logger.info(f"Downloading all videos from channel {channel_url} to {output_directory}")
        # Implement channel download logic here

class DownloadPlaylistCommand(DownloadCommand):
    def execute(self, **kwargs):
        playlist_url = kwargs.get('playlist_url')
        output_directory = kwargs.get('output_directory')
        logger.info(f"Downloading all videos from playlist {playlist_url} to {output_directory}")
        # Implement playlist download logic here
