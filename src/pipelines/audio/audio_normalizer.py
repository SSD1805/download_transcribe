# src/pipelines/audio/audio_normalizer.py
from pydub import effects
from src.pipelines.audio.audio_processor_base import AudioProcessorBase
from src.core.services import CoreServices

logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

class AudioNormalizer(AudioProcessorBase):
    def normalize(self, input_file, output_file):
        audio = self.load_audio(input_file)
        normalized_audio = effects.normalize(audio)
        return self.save_audio(normalized_audio, output_file)
