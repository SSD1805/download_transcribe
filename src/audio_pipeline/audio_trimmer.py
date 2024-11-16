import os
from pydub import AudioSegment
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

log_manager = LoggerManager()
logger = log_manager.get_logger()
perf_tracker = PerformanceTracker

class AudioTrimmer:
    def __init__(self, output_directory='/app/processed_audio', format='wav'):
        self.output_directory = output_directory
        self.format = format
        os.makedirs(self.output_directory, exist_ok=True)
        logger.info(f"AudioTrimmer initialized with output directory: {self.output_directory}")

    @perf_tracker.track_performance
    def trim(self, input_file):
        try:
            audio = AudioSegment.from_file(input_file)
            trimmed_audio = audio.strip_silence(silence_thresh=audio.dBFS - 16)
            output_file = os.path.join(self.output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}_trimmed.{self.format}")
            trimmed_audio.export(output_file, format=self.format)
            logger.info(f"Trimmed audio saved as {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error trimming silence from {input_file}: {e}")
            return None
