from src.pipelines.audio.audio_processor_base import AudioProcessorBase
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class AudioConverter(AudioProcessorBase):
    def convert(self, input_file, output_file, target_format='wav'):
        self.format = target_format
        try:
            audio = self.load_audio(input_file)
            return self.save_audio(audio, output_file)
        except Exception as e:
            logger.error(f"Error converting {input_file} to {target_format}: {e}")
            raise
