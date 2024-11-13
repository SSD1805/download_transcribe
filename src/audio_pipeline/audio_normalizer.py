import os
from pydub import AudioSegment, effects
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceManager

log_manager = LoggerManager()
logger = log_manager.get_logger()
perf_manager = PerformanceManager()

class AudioNormalizer:
    def __init__(self, output_directory='/app/processed_audio', format='wav'):
        self.output_directory = output_directory
        self.format = format
        os.makedirs(self.output_directory, exist_ok=True)
        logger.info(f"AudioNormalizer initialized with output directory: {self.output_directory}")

    @perf_manager.track_performance
    def normalize(self, input_file):
        try:
            audio = AudioSegment.from_file(input_file)
            normalized_audio = effects.normalize(audio)
            output_file = os.path.join(self.output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}_normalized.{self.format}")
            normalized_audio.export(output_file, format=self.format)
            logger.info(f"Normalized audio saved as {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error normalizing {input_file}: {e}")
            return None
