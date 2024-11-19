import click
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer


@click.group()
def cli():
    """CLI for Downloading Content"""
    pass


@click.command()
@click.argument('url')
@inject
def video(url, downloader=Provide[AppContainer.pipeline_component_registry.provide("youtube_downloader")]):
    """Download a single video."""
    downloader.download_video(url)
    click.echo(f"Downloaded video from URL: {url}")


@click.command()
@click.argument('url')
@inject
def channel(url, downloader=Provide[AppContainer.pipeline_component_registry.provide("youtube_downloader")]):
    """Download all videos from a channel."""
    downloader.download_channel(url)
    click.echo(f"Downloaded channel from URL: {url}")


@click.command()
@click.argument('url')
@inject
def playlist(url, downloader=Provide[AppContainer.pipeline_component_registry.provide("youtube_downloader")]):
    """Download all videos from a playlist."""
    downloader.download_playlist(url)
    click.echo(f"Downloaded playlist from URL: {url}")


@click.command()
@click.argument('urls', nargs=-1)
@click.option('--batch-size', default=3, help="Number of downloads to process simultaneously.")
@inject
def batch(urls, batch_size, downloader=Provide[AppContainer.pipeline_component_registry.provide("youtube_downloader")]):
    """Download multiple videos in batches."""
    downloader.download_batch(urls, batch_size=batch_size)
    click.echo("Batch download completed.")


# Add commands to the CLI
cli.add_command(video)
cli.add_command(channel)
cli.add_command(playlist)
cli.add_command(batch)


if __name__ == '__main__':
    container = AppContainer()
    container.wire(modules=[__name__])

    cli()
