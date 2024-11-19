import click
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer


@click.group()
def cli():
    """CLI for Transcription Tasks"""
    pass


@click.command()
@click.argument('input_directory')
@click.argument('output_directory')
@inject
def transcribe(input_directory, output_directory,
               pipeline=Provide[AppContainer.pipeline_component_registry.provide("transcription_pipeline")]):
    """Run the transcription pipeline."""
    pipeline.set_directories(input_directory, output_directory)
    pipeline.process_files()
    click.echo(f"Transcriptions saved in {output_directory}")


@click.command()
@click.argument('segments')
@click.argument('audio_file')
@click.argument('output_directory')
@click.option('--format', default='txt', help='Output format: txt or json')
@inject
def save_transcription(segments, audio_file, output_directory, format,
                       saver=Provide[AppContainer.pipeline_component_registry.provide("transcription_saver")]):
    """Save transcription segments to a file."""
    saver.save_transcription(segments, audio_file, format=format)
    click.echo(f"Transcription for {audio_file} saved in {output_directory} as {format}")


# Add commands to the CLI
cli.add_command(transcribe)
cli.add_command(save_transcription)

if __name__ == '__main__':
    container = AppContainer()
    container.wire(modules=[__name__])

    cli()
