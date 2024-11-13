# cli_audio.py

import click
from audio_handler import AudioHandler

@click.group()
def cli():
    """Command-line interface for audio processing tasks."""
    pass

@cli.command()
@click.argument('input_file')
@click.option('--output-format', default='wav', help='Format to convert the audio file to.')
def convert(input_file, output_format):
    """Convert an audio file to a different format."""
    handler = AudioHandler()
    result = handler.convert(input_file, output_format)
    click.echo(f"Converted file saved to: {result}")

@cli.command()
@click.argument('input_file')
@click.option('--segment-duration', default=30000, help='Duration of each audio segment in milliseconds.')
def split(input_file, segment_duration):
    """Split an audio file into segments."""
    handler = AudioHandler()
    segments = handler.split(input_file, segment_duration)
    click.echo(f"Audio file split into {len(segments)} segments.")

@cli.command()
@click.argument('input_file')
def normalize(input_file):
    """Normalize an audio file."""
    handler = AudioHandler()
    result = handler.normalize(input_file)
    click.echo(f"Normalized file saved to: {result}")

@cli.command()
@click.argument('input_file')
def trim(input_file):
    """Trim silence from an audio file."""
    handler = AudioHandler()
    result = handler.trim(input_file)
    click.echo(f"Trimmed file saved to: {result}")

if __name__ == '__main__':
    cli()
