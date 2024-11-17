# src/cli/cli_audio.py
import click
from src.pipelines.audio.audio_handler import AudioHandler
from src.pipelines.transcription.transcription_pipeline import TranscriptionPipeline


@click.group()
def cli():
    """CLI for audio processing tasks."""
    pass

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
def normalize(input_file, output_file):
    """Normalize an audio file."""
    handler = AudioHandler()
    result = handler.normalize_audio(input_file, output_file)
    click.echo(f"Normalized file saved at {result}")

@cli.command()
@click.argument('input_file')
@click.argument('chunk_duration', type=int)
@click.argument('output_file_prefix')
def split(input_file, chunk_duration, output_file_prefix):
    """Split an audio file into smaller chunks."""
    handler = AudioHandler()
    result = handler.split_audio(input_file, chunk_duration, output_file_prefix)
    click.echo(f"Audio split into {len(result)} chunks.")

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--silence-thresh', default=-40, help='Silence threshold in dBFS.')
def trim(input_file, output_file, silence_thresh):
    """Trim silence from an audio file."""
    handler = AudioHandler()
    result = handler.trim_audio(input_file, output_file, silence_thresh)
    click.echo(f"Trimmed file saved at {result}")


@click.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--target-format', default='wav', help='Target format for audio conversion.')
def convert(input_file, output_file, target_format):
    """Convert an audio file to a specified format."""
    handler = AudioHandler()
    result = handler.convert_audio(input_file, output_file, target_format)
    click.echo(f"Converted audio file saved at {result}")

@click.command()
@click.argument('input_directory')
@click.argument('output_directory')
def run_pipeline(input_directory, output_directory):
    """Run the transcription pipeline."""
    pipeline = TranscriptionPipeline(input_directory, output_directory)
    pipeline.process_files()

if __name__ == '__main__':
    cli()
