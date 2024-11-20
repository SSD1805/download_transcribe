import click
from dependency_injector.wiring import inject, Provide
from infrastructure.dependency_setup import container

@click.group()
def cli():
    """CLI for Downloading Content"""
    pass

@cli.command()
@click.argument('url')
@inject
def video(url, downloader=Provide[container.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[container.logger]):
    """Download a single video."""
    try:
        logger.info(f"Starting download for video URL: {url}")
        downloader.download_video(url)
        logger.info(f"Download completed for video URL: {url}")
    except Exception as e:
        logger.error(f"Failed to download video from URL {url}: {e}")

@cli.command()
@click.argument('url')
@inject
def channel(url, downloader=Provide[container.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[container.logger]):
    """Download all videos from a channel."""
    try:
        logger.info(f"Starting download for channel URL: {url}")
        downloader.download_channel(url)
        logger.info(f"Download completed for channel URL: {url}")
    except Exception as e:
        logger.error(f"Failed to download channel from URL {url}: {e}")

@cli.command()
@click.argument('url')
@inject
def playlist(url, downloader=Provide[container.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[container.logger]):
    """Download all videos from a playlist."""
    try:
        logger.info(f"Starting download for playlist URL: {url}")
        downloader.download_playlist(url)
        logger.info(f"Download completed for playlist URL: {url}")
    except Exception as e:
        logger.error(f"Failed to download playlist from URL {url}: {e}")

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--batch-size', default=3, help="Number of downloads to process simultaneously.")
@inject
def batch(urls, batch_size, downloader=Provide[container.pipeline_component_registry.provide_pipeline_components().get("youtube_downloader")], logger=Provide[container.logger]):
    """Download multiple videos in batches."""
    try:
        logger.info(f"Starting batch download for {len(urls)} videos with batch size: {batch_size}")
        downloader.download_batch(urls, batch_size=batch_size)
        logger.info(f"Batch download completed for {len(urls)} videos.")
    except Exception as e:
        logger.error(f"Batch download failed: {e}")

if __name__ == '__main__':
    cli()
