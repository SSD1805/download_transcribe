import click
from src.app.cli.commands.base_command import BaseCommand


@click.group(cls=BaseCommand)
def cli():
    """CLI for Transcription Tasks."""
    pass


@cli.command(cls=BaseCommand)
@click.argument("input_directory")
@click.argument("output_directory")
def transcribe(ctx, input_directory, output_directory):
    """Run the transcription pipeline on audio files."""
    ctx.command.transcription_pipeline.set_directories(input_directory, output_directory)
    ctx.command.transcription_pipeline.process_files()


@cli.command(cls=BaseCommand)
@click.argument("segments")
@click.argument("audio_file")
@click.argument("output_directory")
@click.option("--format", default="txt", help="Output format: txt or json")
def save_transcription(ctx, segments, audio_file, output_directory, format):
    """Save transcription segments to a file."""
    ctx.command.transcription_pipeline.save_transcription(segments, audio_file, format=format)


if __name__ == "__main__":
    cli()
