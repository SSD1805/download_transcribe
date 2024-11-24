import click

from src.app.cli.commands.base_command import BaseCommand


@click.group(cls=BaseCommand)
def cli():
    """CLI for Downloading Content."""
    pass


@cli.command(cls=BaseCommand)
@click.argument("url")
def video(ctx, url):
    """Download a single video."""
    ctx.command.downloader.download_video(url)


@cli.command(cls=BaseCommand)
@click.argument("url")
def channel(ctx, url):
    """Download all videos from a channel."""
    ctx.command.downloader.download_channel(url)


@cli.command(cls=BaseCommand)
@click.argument("url")
def playlist(ctx, url):
    """Download all videos from a playlist."""
    ctx.command.downloader.download_playlist(url)


@cli.command(cls=BaseCommand)
@click.argument("urls", nargs=-1)
@click.option(
    "--batch-size", default=3, help="Number of downloads to process simultaneously."
)
def batch(ctx, urls, batch_size):
    """Download multiple videos in batches."""
    ctx.command.downloader.download_batch(urls, batch_size=batch_size)


if __name__ == "__main__":
    cli()
