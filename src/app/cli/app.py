"""
CLI application for YouTube audio downloading, transcription, and batch processing.
"""

import click
from dependency_injector.wiring import inject

from src.infrastructure.app.app_container import AppContainer

# CLI Command Functions


@inject
def download_command(downloader, logger, url):
    """
    Command to handle downloading a single video from YouTube.
    """
    try:
        logger.info(f"Starting download for URL: {url}")
        downloader.download_video(url)
        logger.info(f"Download completed for URL: {url}")
    except Exception as e:
        logger.error(f"Failed to download video from URL {url}: {e}")
        raise


@inject
def transcribe_command(
    transcriber,
    pipeline,
    logger,
    performance_tracker,
    audio_file,
    title,
    use_whisperx,
    fallback_to_whisper,
):
    """
    Command to handle transcribing an audio file.
    """
    try:
        if use_whisperx:
            logger.info(f"Using WhisperX to transcribe audio file: {audio_file}")
            with performance_tracker.track_execution("transcription_pipeline"):
                success = pipeline.transcribe_audio(audio_file, title)
            if not success and fallback_to_whisper:
                logger.warning(
                    f"WhisperX failed. Falling back to Whisper AI for audio file: "
                    f"{audio_file}"
                )
                transcriber.transcribe_audio(audio_file, title)
        else:
            logger.info(f"Using Whisper AI to transcribe audio file: {audio_file}")
            with performance_tracker.track_execution("transcription_pipeline"):
                transcriber.transcribe_audio(audio_file, title)

        logger.info(f"Transcription completed for file: {audio_file}")
    except Exception as e:
        logger.error(f"Transcription failed for {audio_file}: {e}")
        raise


@inject
def batch_process_command(batch_processor, logger, input_directory, output_directory):
    """
    Command to handle batch processing tasks.
    """
    try:
        logger.info(f"Starting batch processing for input directory: {input_directory}")
        batch_processor.process(input_directory, output_directory)
        logger.info(f"Batch processing completed. Output saved in: {output_directory}")
    except Exception as e:
        logger.error(
            f"Batch processing failed for input directory {input_directory}: {e}"
        )
        raise


# CLI Commands with Click


@click.group()
def cli():
    """YouTube Audio Downloader and Transcriber CLI"""


@cli.command()
@click.option(
    "--url",
    prompt="Enter YouTube URL",
    help="YouTube video or channel URL to download.",
)
@click.pass_context
def download(ctx, url):
    """Download video from YouTube"""
    command = ctx.obj.get("download_command")
    command(url)


@cli.command()
@click.argument("audio_file")
@click.option("--title", prompt="Enter video title", help="Title for the audio file.")
@click.option(
    "--use-whisperx",
    is_flag=True,
    default=False,
    help="Use WhisperX for transcription.",
)
@click.option(
    "--fallback-to-whisper",
    is_flag=True,
    default=False,
    help="Use Whisper AI as a fallback if WhisperX fails.",
)
@click.pass_context
def transcribe(ctx, audio_file, title, use_whisperx, fallback_to_whisper):
    """Transcribe the provided audio file"""
    command = ctx.obj.get("transcribe_command")
    command(audio_file, title, use_whisperx, fallback_to_whisper)


@cli.command()
@click.argument("input_directory")
@click.argument("output_directory")
@click.pass_context
def batch_process(ctx, input_directory, output_directory):
    """Process batch tasks for input directory"""
    command = ctx.obj.get("batch_command")
    command(input_directory, output_directory)


# Main Entry Point


@click.pass_context
def setup_context(ctx):
    """
    Set up the dependency context for CLI commands.
    """
    container = AppContainer()
    ctx.ensure_object(dict)

    # Add commands to the context
    ctx.obj["download_command"] = lambda url: download_command(
        container.pipeline_component_registry.provide_pipeline_components()[
            "youtube_downloader"
        ],
        container.struct_logger,
        url,
    )
    ctx.obj["transcribe_command"] = (
        lambda audio_file, title, use_whisperx, fallback_to_whisper: transcribe_command(
            container.transcriber,
            container.pipeline_component_registry.provide_pipeline_components()[
                "transcription_pipeline"
            ],
            container.struct_logger,
            container.tracking_utility,
            audio_file,
            title,
            use_whisperx,
            fallback_to_whisper,
        )
    )
    ctx.obj["batch_command"] = (
        lambda input_directory, output_directory: batch_process_command(
            container.batch_processor,
            container.struct_logger,
            input_directory,
            output_directory,
        )
    )


if __name__ == "__main__":
    cli(obj={})
