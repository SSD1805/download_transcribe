import click
from src.audio_pipeline.audio_converter import AudioConverter

@click.group()
def cli():
    """Audio Processing CLI"""
    pass

@cli.command()
@click.argument('input_file')
@click.option('--output-format', default='wav', help='Format to convert the downloaders file to.')
def convert(input_file, output_format):
    """Convert an downloaders file to a different format."""
    converter = AudioConverter()
    converter.convert_audio_format(input_file, output_format)

@cli.command()
def batch_convert():
    """Batch convert all downloaders files in the input directory."""
    converter = AudioConverter()
    converter.batch_convert_audio_files()

if __name__ == "__main__":
    cli()


class AudioCLI:
    pass