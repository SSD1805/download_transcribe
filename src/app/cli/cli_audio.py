import click

from src.app.cli.commands.base_command import BaseCommand


@click.group(cls=BaseCommand)
def cli():
    """CLI for Audio Processing Tasks."""
    pass


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("output_file")
def normalize(ctx, input_file, output_file):
    """Normalize an audio file."""
    ctx.command.audio_processor.normalize(input_file, output_file)


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("chunk_duration", type=int)
@click.argument("output_file_prefix")
def split(ctx, input_file, chunk_duration, output_file_prefix):
    """Split an audio file into chunks."""
    ctx.command.audio_processor.split(input_file, chunk_duration, output_file_prefix)


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("output_file")
@click.option("--silence-thresh", default=-40, help="Silence threshold in dBFS.")
def trim(ctx, input_file, output_file, silence_thresh):
    """Trim silence from an audio file."""
    ctx.command.audio_processor.trim(input_file, output_file, silence_thresh)


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("output_file")
@click.option(
    "--target-format", default="wav", help="Target format for audio conversion."
)
def convert(ctx, input_file, output_file, target_format):
    """Convert an audio file to a specified format."""
    ctx.command.audio_processor.convert(input_file, output_file, target_format)


if __name__ == "__main__":
    cli()
