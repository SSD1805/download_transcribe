from celery import shared_task
from src.core.logger_manager import LoggerManager
from src.transcription_pipeline.audio_transcriber import AudioTranscriber
from src.download_pipeline.custom_exceptions import ConfigurationError
from src.transcription_pipeline.transcription_saver import TranscriptionSaver
from src.core.performance_tracker import PerformanceTracker

logger = LoggerManager().get_logger()
performance_tracker = PerformanceTracker()


@shared_task(bind=True, max_retries=3)
def transcribe_audio_task(self, audio_file_path):
    """
    Celery task to transcribe an audio file.

    Args:
        self:
        audio_file_path (str): The file path of the audio to transcribe.

    Raises:
        ConfigurationError: If transcription setup fails.
    """
    try:
        logger.info(f"Starting transcription task for audio file: {audio_file_path}")

        # Start tracking the task
        with performance_tracker.track_execution("Transcription Task"):
            # Perform transcription
            transcriber = AudioTranscriber()
            segments = transcriber.transcribe(audio_file_path)

            # Save the transcription result
            with performance_tracker.track_execution("Save Transcription Task"):
                TranscriptionSaver().save_transcription(segments, audio_file_path)

        logger.info(f"Transcription completed and saved for file: {audio_file_path}")
        return segments

    except ConfigurationError as e:
        logger.error(f"Transcription failed for file: {audio_file_path} with error: {e}")
        self.retry(countdown=120, exc=e)  # Retry in 2 minutes if it fails
