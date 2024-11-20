from dask.distributed import Client

from src.pipelines.audio.audio_converter import AudioConverter

# Get logger and performance tracker from CoreServices
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


# Initialize Dask client, logger, and performance tracker
client = Client()


def convert_audio(file_path):
    """
    Convert audio_processor file to WAV format if necessary.

    Args:
        file_path (str): Path to the audio_processor file.

    Returns:
        str: Path to the converted WAV file or original path if already WAV.
    """
    converter = AudioConverter()
    return converter.convert_to_wav(file_path) or file_path  # Return original path if already WAV


client.register_worker_plugin(convert_audio)  # Register function as plugin

if __name__ == "__main__":
    client.run(convert_audio, "/data/audio_files/file.mp3")  # Sample execution
