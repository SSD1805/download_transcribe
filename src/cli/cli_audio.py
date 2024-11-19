import click
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer


@click.group()
def cli():
    """CLI for audio processing tasks."""
    pass


@click.command()
@click.argument('input_file')
@click.argument('output_file')
@inject
def normalize(input_file, output_file, handler=Provide[AppContainer.pipeline_component_registry.provide("audio_handler")]):
    """Normalize an audio file."""
    result = handler.normalize_audio(input_file, output_file)
    click.echo(f"Normalized file saved at {result}")


@click.command()
@click.argument('input_file')
@click.argument('chunk_duration', type=int)
@click.argument('output_file_prefix')
@inject
def split(input_file, chunk_duration, output_file_prefix, handler=Provide[AppContainer.pipeline_component_registry.provide("audio_handler")]):
    """Split an audio file into smaller chunks."""
    result = handler.split_audio(input_file, chunk_duration, output_file_prefix)
    click.echo(f"Audio split into {len(result)} chunks.")


@click.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--silence-thresh', default=-40, help='Silence threshold in dBFS.')
@inject
def trim(input_file, output_file, silence_thresh, handler=Provide[AppContainer.pipeline_component_registry.provide("audio_handler")]):
    """Trim silence from an audio file."""
    result = handler.trim_audio(input_file, output_file, silence_thresh)
    click.echo(f"Trimmed file saved at {result}")


@click.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--target-format', default='wav', help='Target format for audio conversion.')
@inject
def convert(input_file, output_file, target_format, handler=Provide[AppContainer.pipeline_component_registry.provide("audio_handler")]):
    """Convert an audio file to a specified format."""
    result = handler.convert_audio(input_file, output_file, target_format)
    click.echo(f"Converted audio file saved at {result}")


@click.command()
@click.argument('input_directory')
@click.argument('output_directory')
@inject
def run_pipeline(input_directory, output_directory, pipeline=Provide[AppContainer.pipeline_component_registry.provide("transcription_pipeline")]):
    """Run the transcription pipeline."""
    pipeline.set_directories(input_directory, output_directory)
    pipeline.process_files()


# Add commands to the CLI
cli.add_command(normalize)
cli.add_command(split)
cli.add_command(trim)
cli.add_command(convert)
cli.add_command(run_pipeline)


if __name__ == '__main__':
    # Initialize the container
    container = AppContainer()
    container.wire(modules=[__name__])

    cli()
