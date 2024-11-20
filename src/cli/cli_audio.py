import click
from dependency_injector.wiring import inject, Provide
from src.infrastructure.dependency_setup import container

@click.group()
def cli():
    """CLI for Audio Processing Tasks"""
    pass

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@inject
def normalize(input_file, output_file, handler=Provide[container.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[container.logger]):
    """Normalize an audio file."""
    try:
        logger.info(f"Normalizing audio file: {input_file}")
        result = handler.normalize_audio(input_file, output_file)
        logger.info(f"Normalization completed. Output file: {result}")
    except Exception as e:
        logger.error(f"Failed to normalize audio file {input_file}: {e}")

@cli.command()
@click.argument('input_file')
@click.argument('chunk_duration', type=int)
@click.argument('output_file_prefix')
@inject
def split(input_file, chunk_duration, output_file_prefix, handler=Provide[container.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[container.logger]):
    """Split an audio file into smaller chunks."""
    try:
        logger.info(f"Splitting audio file: {input_file} into chunks of {chunk_duration} seconds.")
        result = handler.split_audio(input_file, chunk_duration, output_file_prefix)
        logger.info(f"Audio split into {len(result)} chunks.")
    except Exception as e:
        logger.error(f"Failed to split audio file {input_file}: {e}")

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--silence-thresh', default=-40, help='Silence threshold in dBFS.')
@inject
def trim(input_file, output_file, silence_thresh, handler=Provide[container.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[container.logger]):
    """Trim silence from an audio file."""
    try:
        logger.info(f"Trimming silence from audio file: {input_file}")
        result = handler.trim_audio(input_file, output_file, silence_thresh)
        logger.info(f"Silence trimmed. Output file: {result}")
    except Exception as e:
        logger.error(f"Failed to trim audio file {input_file}: {e}")

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--target-format', default='wav', help='Target format for audio conversion.')
@inject
def convert(input_file, output_file, target_format, handler=Provide[container.pipeline_component_registry.provide_pipeline_components().get("audio_handler")], logger=Provide[container.logger]):
    """Convert an audio file to a specified format."""
    try:
        logger.info(f"Converting audio file: {input_file} to format: {target_format}")
        result = handler.convert_audio(input_file, output_file, target_format)
        logger.info(f"Conversion completed. Output file: {result}")
    except Exception as e:
        logger.error(f"Failed to convert audio file {input_file}: {e}")

@cli.command()
@click.argument('input_directory')
@click.argument('output_directory')
@inject
def run_pipeline(input_directory, output_directory, pipeline=Provide[container.transcriber], logger=Provide[container.logger]):
    """Run the transcription pipeline."""
    try:
        logger.info(f"Running transcription pipeline for directory: {input_directory}")
        pipeline.set_directories(input_directory, output_directory)
        pipeline.process_files()
        logger.info(f"Transcription pipeline completed for directory: {input_directory}")
    except Exception as e:
        logger.error(f"Failed to run transcription pipeline for directory {input_directory}: {e}")

if __name__ == '__main__':
    cli()
