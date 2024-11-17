# src/pipelines/audio/audio_splitter.py
from src.core.services import CoreServices

logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


class AudioSplitter(AudioProcessorBase):
    def split(self, input_file, chunk_duration_ms, output_file_prefix):
        audio = self.load_audio(input_file)
        chunks = [audio[i:i + chunk_duration_ms] for i in range(0, len(audio), chunk_duration_ms)]
        chunk_files = []
        for idx, chunk in enumerate(chunks):
            chunk_file = f"{output_file_prefix}_chunk{idx}.{self.format}"
            chunk_files.append(self.save_audio(chunk, chunk_file))
        return chunk_files
