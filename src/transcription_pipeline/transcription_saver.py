import os
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize logger and performance tracker
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()

class TranscriptionSaver:
    def __init__(self, output_directory='/app/transcriptions'):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    @perf_tracker.track  # Decorator to measure performance of the save_transcription method
    def save_transcription(self, segments, audio_file):
        output_file = os.path.join(self.output_directory, f"{os.path.splitext(os.path.basename(audio_file))[0]}.txt")
        try:
            with open(output_file, 'w') as f:
                for segment in segments:
                    f.write(f"{segment['text']}\n")
            logger.info(f"Transcription saved as '{output_file}'.")
        except Exception as e:
            logger.error(f"Error saving transcription for '{audio_file}': {e}")
