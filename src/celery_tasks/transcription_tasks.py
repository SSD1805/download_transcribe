from celery import shared_task
from dependency_injector.wiring import inject, Provide
from src.infrastructure.dependency_setup import container

@shared_task(bind=True, max_retries=3)
@inject
def transcribe_audio_task(
    self,
    audio_file_path: str,
    logger=Provide[container.logger],
    performance_tracker=Provide[container.performance_tracker],
    audio_transcriber=Provide[container.transcriber],
    transcription_saver=Provide[container.pipeline_component_registry.provide_pipeline_components().get("transcription_saver")]
):
    """
    Celery task to transcribe an audio file.

    Args:
        audio_file_path (str): The file path of the audio to transcribe.
        logger: Logger instance for logging (injected).
        performance_tracker: Performance tracker instance for tracking execution (injected).
        audio_transcriber: AudioTranscriber instance for transcribing audio (injected).
        transcription_saver: TranscriptionSaver instance for saving transcriptions (injected).
    """
    try:
        logger.info(f"Starting transcription task for audio file: {audio_file_path}")

        # Track the transcription task
        with performance_tracker.track_execution("Transcription Task"):
            segments = audio_transcriber.transcribe(audio_file_path)

        # Track the save transcription task
        with performance_tracker.track_execution("Save Transcription Task"):
            transcription_saver.save_transcription(segments, audio_file_path)

        logger.info(f"Transcription completed and saved for file: {audio_file_path}")
        return segments

    except Exception as e:
        logger.error(f"Transcription failed for file: {audio_file_path} with error: {e}")
        raise self.retry(countdown=120, exc=e)
