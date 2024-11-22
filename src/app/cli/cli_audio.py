import click
from src.app.cli.commands.base_command import BaseCommand


@click.group(cls=BaseCommand)
def cli():
    """CLI for Audio Processing Tasks."""
    pass


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("output_file")
def normalize(input_file, output_file):
    """Normalize an audio file."""
    from src.app.pipelines.audio.audio_normalizer import AudioNormalizer
    normalizer = AudioNormalizer()
    normalizer.execute(input_file, output_file)


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("chunk_duration", type=int)
@click.argument("output_file_prefix")
def split(input_file, chunk_duration, output_file_prefix):
    """Split an audio file into chunks."""
    from src.app.pipelines.audio.audio_splitter import AudioSplitter
    splitter = AudioSplitter()
    splitter.execute(input_file, chunk_duration, output_file_prefix)


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("output_file")
@click.option("--silence-thresh", default=-40, help="Silence threshold in dBFS.")
def trim(input_file, output_file, silence_thresh):
    """Trim silence from an audio file."""
    from src.app.pipelines.audio.audio_trimmer import AudioTrimmer
    trimmer = AudioTrimmer()
    trimmer.execute(input_file, output_file, silence_thresh)


@cli.command(cls=BaseCommand)
@click.argument("input_file")
@click.argument("output_file")
@click.option("--target-format", default="wav", help="Target format for audio conversion.")
def convert(input_file, output_file, target_format):
    """Convert an audio file to a specified format."""
    from src.app.pipelines.audio.audio_converter import AudioConverter
    converter = AudioConverter()
    converter.execute(input_file, output_file, target_format)


if __name__ == "__main__":
    cli()
