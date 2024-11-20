import click
from dependency_injector.wiring import inject, Provide
from src.infrastructure.dependency_setup import container

@click.group()
def cli():
    """CLI for Transcription Tasks"""
    pass

@cli.command()
@click.argument('input_directory')
@click.argument('output_directory')
@inject
def transcribe(
        input_directory,
        output_directory,
        pipeline=Provide[container.pipeline_component_registry.provide_pipeline_components().get("transcription_pipeline")],
        logger=Provide[container.logger],
        performance_tracker=Provide[container.performance_tracker]
    ):
    """Run the transcription pipeline on audio files."""
    try:
        logger.info(f"Starting transcription for directory: {input_directory}")
        with performance_tracker.track_execution("transcription_pipeline"):
            pipeline.set_directories(input_directory, output_directory)
            pipeline.process_files()
        logger.info(f"Transcription completed. Output saved in: {output_directory}")
    except Exception as e:
        logger.error(f"Transcription failed for directory {input_directory}: {e}")

@cli.command()
@click.argument('segments')
@click.argument('audio_file')
@click.argument('output_directory')
@click.option('--format', default='txt', help='Output format: txt or json')
@inject
def save_transcription(
        segments,
        audio_file,
        output_directory,
        format,
        saver=Provide[container.pipeline_component_registry.provide_pipeline_components().get("transcription_saver")],
        logger=Provide[container.logger]
    ):
    """Save transcription segments to a file."""
    try:
        logger.info(f"Saving transcription for audio file: {audio_file} to {output_directory} in format: {format}")
        saver.save_transcription(segments, audio_file, format=format)
        logger.info(f"Transcription saved for {audio_file} in {output_directory} as {format}")
    except Exception as e:
        logger.error(f"Failed to save transcription for {audio_file}: {e}")

if __name__ == '__main__':
    container.wire(modules=[__name__])
    cli()
