from dask.distributed import Client
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer

# Initialize Dask client
client = Client()

@inject
def convert_audio(
    file_path: str,
    logger=Provide[AppContainer.logger],
    perf_tracker=Provide[AppContainer.performance_tracker],
    audio_converter=Provide[AppContainer.audio_converter]
):
    """
    Convert an audio file to WAV format if necessary.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        str: Path to the converted WAV file or original path if already WAV.
    """
    try:
        with perf_tracker.track_execution("Audio Conversion Task"):
            logger.info(f"Starting audio conversion for file: {file_path}")
            result = audio_converter.convert_to_wav(file_path)
            logger.info(f"Audio conversion completed for file: {file_path}")
            return result or file_path  # Return original path if already WAV
    except Exception as e:
        logger.error(f"Error during audio conversion for file {file_path}: {e}")
        raise

if __name__ == "__main__":
    # Wire the dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])

    # Example usage: submitting an audio conversion task
    sample_audio_file = "/data/audio_files/file.mp3"
    future = client.submit(convert_audio, sample_audio_file)
    print(future.result())
