from dask.distributed import Client
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker
from src.audio_pipeline.audio_converter import convert_audio
from src.transcription_pipeline.audio_transcriber import transcribe_audio

# Initialize Dask client, logger, and performance tracker
client = Client("tcp://dask_scheduler:8786")
logger = LoggerManager().get_logger(__name__)
perf_tracker = PerformanceTracker()


def execute_pipeline():
    """
    Executes the audio processing pipeline, including audio conversion and transcription tasks.
    """
    # Track the overall pipeline execution time
    with perf_tracker.track_execution("Audio Processing Pipeline"):
        try:
            # Schedule audio conversion task
            logger.info("Scheduling audio conversion task.")
            future_conversion = client.submit(convert_audio, "/app/audio_files/file.mp3")

            # Schedule transcription task
            logger.info("Scheduling transcription task.")
            future_transcription = client.submit(transcribe_audio, "/app/audio_files/file.wav")

            # Retrieve and log results with performance tracking for each task
            with perf_tracker.track_execution("Audio Conversion Task"):
                result_conversion = future_conversion.result()
                logger.info(f"Audio conversion completed successfully: {result_conversion}")

            with perf_tracker.track_execution("Audio Transcription Task"):
                result_transcription = future_transcription.result()
                logger.info(f"Audio transcription completed successfully: {result_transcription}")

        except Exception as e:
            logger.error(f"Error in processing pipeline: {e}")
            raise


if __name__ == "__main__":
    execute_pipeline()
