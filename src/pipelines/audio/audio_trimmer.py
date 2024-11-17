# src/pipelines/audio/audio_trimmer.py
from src.core.services import CoreServices

logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


class AudioTrimmer(AudioProcessorBase):
    def trim(self, input_file, output_file, silence_thresh=-40):
        audio = self.load_audio(input_file)
        trimmed_audio = audio.strip_silence(silence_thresh=silence_thresh)
        return self.save_audio(trimmed_audio, output_file)
