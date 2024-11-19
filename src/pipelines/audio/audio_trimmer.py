from src.pipelines.audio.audio_processor_base import AudioProcessorBase
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class AudioTrimmer(AudioProcessorBase):
    def trim(self, input_file, output_file, silence_thresh=-40):
        try:
            audio = self.load_audio(input_file)
            trimmed_audio = audio.strip_silence(silence_thresh=silence_thresh)
            return self.save_audio(trimmed_audio, output_file)
        except Exception as e:
            logger.error(f"Error trimming audio file {input_file}: {e}")
            raise
