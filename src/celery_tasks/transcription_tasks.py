from celery import shared_task
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker
from src.pipelines.transcription.audio_transcriber import AudioTranscriber
from src.pipelines.transcription.transcription_saver import TranscriptionSaver
from src.infrastructure.registries import ErrorRegistry

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

@shared_task(bind=True, max_retries=3)
def transcribe_audio_task(self, audio_file_path):
    """
    Celery task to transcribe an audio_processor file.

    Args:
        audio_file_path (str): The file path of the audio_processor to transcribe.

    Raises:
        ConfigurationError: If transcription setup fails.
    """
    try:
        logger.info(f"Starting transcription task for audio_processor file: {audio_file_path}")
        with perf_tracker.track_execution("Transcription Task"):
            transcriber = AudioTranscriber()
            segments = transcriber.transcribe(audio_file_path)

            with perf_tracker.track_execution("Save Transcription Task"):
                TranscriptionSaver().save_transcription(segments, audio_file_path)

        logger.info(f"Transcription completed and saved for file: {audio_file_path}")
        return segments

    except ErrorRegistry as e:
        logger.error(f"Transcription failed for file: {audio_file_path} with error: {e}")
        self.retry(countdown=120, exc=e)
