import click
from .commands.base_command import BaseCommand
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer

# Command Classes for Different Download Tasks

class DownloadVideoCommand(BaseCommand):
    """
    Command to handle downloading a single video.
    """

    @inject
    def __init__(self, downloader=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[AppContainer.struct_logger]):
        self.downloader = downloader
        self.logger = logger

    def execute(self, url):
        try:
            self.logger.info(f"Starting download for video URL: {url}")
            self.downloader.download_video(url)
            self.logger.info(f"Download completed for video URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed to download video from URL {url}: {e}")
            raise

class DownloadChannelCommand(BaseCommand):
    """
    Command to handle downloading all videos from a channel.
    """

    @inject
    def __init__(self, downloader=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[AppContainer.struct_logger]):
        self.downloader = downloader
        self.logger = logger

    def execute(self, url):
        try:
            self.logger.info(f"Starting download for channel URL: {url}")
            self.downloader.download_channel(url)
            self.logger.info(f"Download completed for channel URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed to download channel from URL {url}: {e}")
            raise

class DownloadPlaylistCommand(BaseCommand):
    """
    Command to handle downloading all videos from a playlist.
    """

    @inject
    def __init__(self, downloader=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[AppContainer.struct_logger]):
        self.downloader = downloader
        self.logger = logger

    def execute(self, url):
        try:
            self.logger.info(f"Starting download for playlist URL: {url}")
            self.downloader.download_playlist(url)
            self.logger.info(f"Download completed for playlist URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed to download playlist from URL {url}: {e}")
            raise

class BatchDownloadCommand(BaseCommand):
    """
    Command to handle downloading multiple videos in batches.
    """

    @inject
    def __init__(self, downloader=Provide[AppContainer.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[AppContainer.struct_logger]):
        self.downloader = downloader
        self.logger = logger

    def execute(self, urls, batch_size):
        try:
            self.logger.info(f"Starting batch download for {len(urls)} videos with batch size: {batch_size}")
            self.downloader.download_batch(urls, batch_size=batch_size)
            self.logger.info(f"Batch download completed for {len(urls)} videos.")
        except Exception as e:
            self.logger.error(f"Batch download failed: {e}")
            raise

# CLI Commands with Click

@click.group()
def cli():
    """CLI for Downloading Content"""
    pass

@cli.command()
@click.argument('url')
@click.pass_context
def video(ctx, url):
    """Download a single video."""
    command = ctx.obj.get('video_command')
    command.execute(url)

@cli.command()
@click.argument('url')
@click.pass_context
def channel(ctx, url):
    """Download all videos from a channel."""
    command = ctx.obj.get('channel_command')
    command.execute(url)

@cli.command()
@click.argument('url')
@click.pass_context
def playlist(ctx, url):
    """Download all videos from a playlist."""
    command = ctx.obj.get('playlist_command')
    command.execute(url)

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--batch-size', default=3, help="Number of downloads to process simultaneously.")
@click.pass_context
def batch(ctx, urls, batch_size):
    """Download multiple videos in batches."""
    command = ctx.obj.get('batch_command')
    command.execute(urls, batch_size)

# Main Entry Point
@click.pass_context
def setup_context(ctx):
    """
    Set up the dependency context for CLI commands.
    """
    container = AppContainer()
    ctx.ensure_object(dict)

    # Instantiate command classes and add them to the context
    ctx.obj['video_command'] = DownloadVideoCommand()
    ctx.obj['channel_command'] = DownloadChannelCommand()
    ctx.obj['playlist_command'] = DownloadPlaylistCommand()
    ctx.obj['batch_command'] = BatchDownloadCommand()

# Inject the setup_context to initialize commands
if __name__ == '__main__':
    cli(obj={})  # Initialize with an empty context dictionary and let Click pass it to commands
