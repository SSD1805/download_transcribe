import click
from src.audio_pipeline.audio_converter import AudioConverter

@click.group()
def cli():
    """Audio Processing CLI"""
    pass

@cli.command()
@click.argument('input_file')
@click.option('--output-format', default='wav', help='Format to convert the audio_pipeline file to.')
def convert(input_file, output_format):
    """Convert an audio_pipeline file to a different format."""
    converter = AudioConverter()
    converter.convert_audio_format(input_file, output_format)

@cli.command()
def batch_convert():
    """Batch convert all audio_pipeline files in the input directory."""
    converter = AudioConverter()
    converter.batch_convert_audio_files()

if __name__ == "__main__":
    cli()


class AudioCLI:
    pass