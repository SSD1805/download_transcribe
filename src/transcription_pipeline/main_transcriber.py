import os
from tqdm import tqdm
from src.audio_pipeline.audio_converter import AudioConverter
from src.transcription_pipeline.audio_transcriber import AudioTranscriber
from src.transcription_pipeline.transcription_saver import TranscriptionSaver
from src.core.performance_tracker import PerformanceTracker
from src.core.logger_manager import LoggerManager

# Initialize performance manager and logger
perf_tracker = PerformanceTracker()
log_manager = LoggerManager()
logger = log_manager.get_logger()


@perf_tracker.track_performance
def process_audio_files(input_directory='/app/audio_files'):
    """
    Process audio files in the specified directory, converting to WAV if necessary,
    transcribing the content, and saving the transcription.

    Args:
        input_directory (str): The directory containing audio files to process.
    """
    converter = AudioConverter()
    transcriber = AudioTranscriber()
    saver = TranscriptionSaver()

    # Find all audio files with specified extensions
    audio_files = [f for f in os.listdir(input_directory) if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]

    for file_name in tqdm(audio_files, desc="Processing audio files"):
        input_path = os.path.join(input_directory, file_name)

        # Convert to WAV format if necessary
        if not file_name.endswith('.wav'):
            wav_file = converter.convert_to_wav(input_path)
            if not wav_file:
                logger.warning(f"Skipping '{file_name}' due to conversion error.")
                continue
        else:
            wav_file = input_path

        # Transcribe the WAV file and save the transcription
        try:
            segments = transcriber.transcribe(wav_file)
            saver.save_transcription(segments, file_name)
            logger.info(f"Successfully processed and saved transcription for '{file_name}'.")
        except Exception as e:
            logger.error(f"Error processing file '{file_name}': {e}")


if __name__ == "__main__":
    # Start monitoring memory usage if needed
    perf_tracker.monitor_memory_usage()
    process_audio_files()
