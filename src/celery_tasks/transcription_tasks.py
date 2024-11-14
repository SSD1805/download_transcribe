# celery_tasks/transcription_tasks.py

from celery import shared_task
from src.core.logger_manager import LoggerManager
from src.transcription_pipeline.audio_transcriber import AudioTranscriber
from src.download_pipeline.custom_exceptions import ConfigurationError

logger = LoggerManager().get_logger()


@shared_task(bind=True, max_retries=3)
def transcribe_audio_task(self, audio_file_path):
    """
    Celery task to transcribe an audio file.

    Args:
        audio_file_path (str): The file path of the audio to transcribe.

    Raises:
        ConfigurationError: If transcription setup fails.
    """
    try:
        logger.info(f"Starting transcription task for audio file: {audio_file_path}")
        transcriber = AudioTranscriber()
        segments = transcriber.transcribe(audio_file_path)

        # Save the transcription result
        TranscriptionSaver().save_transcription(segments, audio_file_path)
        logger.info(f"Transcription completed and saved for file: {audio_file_path}")

        return segments
    except ConfigurationError as e:
        logger.error(f"Transcription failed for file: {audio_file_path} with error: {e}")
        self.retry(countdown=120, exc=e)  # Retry in 2 minutes if it fails
