# src/pipelines/audio/audio_normalizer.py
from pydub import pydub
from src.pipelines.audio.audio_processor_base import AudioProcessorBase
from src.utils.logger_service import LoggerService
from src.utils.performance_tracker import PerformanceTrackerService

logger = LoggerService.get_logger()
perf_tracker = PerformanceTrackerService.get_performance_tracker()

class AudioNormalizer(AudioProcessorBase):
    def normalize(self, input_file, output_file):
        audio = self.load_audio(input_file)
        normalized_audio = effects.normalize(audio)
        return self.save_audio(normalized_audio, output_file)
