from dask.distributed import Client, worker
from src.audio_pipeline.audio_converter import AudioConverter
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker


# Initialize Dask client, logger, and performance tracker
client = Client()
logger = LoggerManager().get_logger(__name__)
perf_tracker = PerformanceTracker()

def convert_audio(file_path):
    """
    Convert audio file to WAV format if necessary.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        str: Path to the converted WAV file or original path if already WAV.
    """
    converter = AudioConverter()
    return converter.convert_to_wav(file_path) or file_path  # Return original path if already WAV


client.register_worker_plugin(convert_audio)  # Register function as plugin

if __name__ == "__main__":
    client.run(convert_audio, "/app/audio_files/file.mp3")  # Sample execution
