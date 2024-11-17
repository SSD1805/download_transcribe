from dask.distributed import Client
from src.pipelines.transcription.audio_transcriber import AudioTranscriber
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

# Initialize Dask client, logger, and performance tracker
client = Client()

def transcribe_audio(file_path):
    """
    Transcribe an audio file with logging and performance tracking.

    Args:
        file_path (str): Path to the WAV file.

    Returns:
        list: List of transcription segments.
    """
    transcriber = AudioTranscriber()

    with perf_tracker.track_execution("Audio Transcription"):
        logger.info(f"Starting transcription task for file: {file_path}")
        try:
            result = transcriber.transcribe(file_path)
            logger.info(f"Transcription completed successfully for file: {file_path}")
            return result
        except Exception as e:
            logger.error(f"Error during transcription of {file_path}: {e}")
            raise

client.register_worker_plugin(transcribe_audio)

if __name__ == "__main__":
    sample_file_path = "/data/audio_files/file.wav"
    future = client.submit(transcribe_audio, sample_file_path)
    print(future.result())
