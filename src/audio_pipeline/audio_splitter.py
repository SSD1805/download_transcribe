import os
from pydub import AudioSegment
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceManager

log_manager = LoggerManager()
logger = log_manager.get_logger()
perf_manager = PerformanceManager()

class AudioSplitter:
    def __init__(self, output_directory='/app/processed_audio', format='wav'):
        self.output_directory = output_directory
        self.format = format
        os.makedirs(self.output_directory, exist_ok=True)
        logger.info(f"AudioSplitter initialized with output directory: {self.output_directory}")

    @perf_manager.track_performance
    def split(self, input_file, segment_duration=30000):
        try:
            audio = AudioSegment.from_file(input_file)
            segments = []
            for i in range(0, len(audio), segment_duration):
                segment = audio[i:i + segment_duration]
                segment_file = os.path.join(self.output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}_part_{i // segment_duration}.{self.format}")
                segment.export(segment_file, format=self.format)
                segments.append(segment_file)
                logger.info(f"Segmented audio saved as {segment_file}")
            return segments
        except Exception as e:
            logger.error(f"Error splitting {input_file}: {e}")
            return []
