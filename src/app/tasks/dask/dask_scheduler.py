from dask.distributed import Client

from src.app.pipelines.audio_processing.audio_converter import AudioConverter
from src.app.pipelines.transcription.audio_to_text_transcriber import AudioTranscriber
from src.app.utils.performance_and_progress_tracking import PerformanceTrackerService
from src.app.utils.application_logger import LoggerService

# Get logger and performance tracker from CoreServices
logger = LoggerService.get_logger()
perf_tracker = PerformanceTrackerService.get_performance_tracker()

# Initialize Dask client, logger, and performance tracker
client = Client("tcp://dask_scheduler:8786")


def execute_pipeline(input_file, output_file):
    """
    Executes the audio_processor processing pipeline, including audio_processor conversion and transcription tasks.

    Args:
        input_file (str): Path to the input audio_processor file (e.g., MP3).
        output_file (str): Path to save the transcription output (e.g., TXT).
    """
    # Track the overall pipeline execution time
    with perf_tracker.track_execution("Audio Processing Pipeline"):
        try:
            # Instantiate pipeline components
            audio_converter = AudioConverter()
            audio_transcriber = AudioTranscriber()

            # Schedule audio_processor conversion task
            logger.info(f"Scheduling audio_processor conversion for file: {input_file}")
            future_conversion = client.submit(audio_converter.convert_audio, input_file)

            # Schedule transcription task (depends on audio_processor conversion result)
            logger.info(
                "Scheduling transcription task after audio_processor conversion."
            )
            future_transcription = client.submit(
                audio_transcriber.transcribe, future_conversion.result()
            )

            # Retrieve and log results with performance tracking for each task
            with perf_tracker.track_execution("Audio Conversion Task"):
                converted_file = future_conversion.result()
                logger.info(
                    f"Audio conversion completed successfully: {converted_file}"
                )

            with perf_tracker.track_execution("Audio Transcription Task"):
                transcription_result = future_transcription.result()
                logger.info(
                    f"Audio transcription completed successfully: {transcription_result}"
                )

            # Save transcription output
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcription_result)
            logger.info(f"Transcription saved to {output_file}.")

        except Exception as e:
            logger.error(f"Error in processing pipeline: {e}")
            raise


if __name__ == "__main__":
    # Example input/output files
    input_audio_file = "/data/audio_files/file.mp3"
    transcription_output_file = "/data/audio_files/transcription.txt"

    execute_pipeline(input_audio_file, transcription_output_file)
