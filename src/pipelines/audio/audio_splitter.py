# This module contains the AudioSplitter class, which is responsible for splitting an audio file into smaller chunks.
from src.pipelines.audio.audio_processor_base import AudioProcessorBase
from src.utils.structlog_logger import StructLogger
from src.utils.tracking_utilities import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()


class AudioSplitter(AudioProcessorBase):
    def split(self, input_file, chunk_duration_ms, output_file_prefix):
        try:
            audio = self.load_audio(input_file)
            chunks = [audio[i:i + chunk_duration_ms] for i in range(0, len(audio), chunk_duration_ms)]
            chunk_files = []
            for idx, chunk in enumerate(chunks):
                chunk_file = f"{output_file_prefix}_chunk{idx}.{self.format}"
                chunk_files.append(self.save_audio(chunk, chunk_file))
            logger.info(f"Split audio into {len(chunk_files)} chunks.")
            return chunk_files
        except Exception as e:
            logger.error(f"Error splitting audio file {input_file}: {e}")
            raise
