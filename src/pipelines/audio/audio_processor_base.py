# src/pipelines/audio/audio_processor_base.py
import os
from pydub import AudioSegment
from src.core.services import CoreServices

logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

class AudioProcessorBase:
    def __init__(self, output_directory, format='wav'):
        self.output_directory = output_directory
        self.format = format
        os.makedirs(self.output_directory, exist_ok=True)

    def load_audio(self, input_file):
        try:
            return AudioSegment.from_file(input_file)
        except Exception as e:
            logger.error(f"Error loading audio file {input_file}: {e}")
            raise

    def save_audio(self, audio, output_file):
        output_path = os.path.join(self.output_directory, output_file)
        try:
            audio.export(output_path, format=self.format)
            logger.info(f"Audio saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving audio file {output_file}: {e}")
            raise
