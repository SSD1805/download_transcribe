# src/pipelines/audio/audio_converter.py
from src.pipelines.audio.audio_processor_base import AudioProcessorBase
from src.core.services import CoreServices

logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()



class AudioConverter(AudioProcessorBase):
    def convert(self, input_file, output_file, target_format='wav'):
        """
        Converts an audio file to the specified format.

        Args:
            input_file (str): Path to the input audio file.
            output_file (str): Path to save the converted audio file.
            target_format (str): The target format for conversion (e.g., 'wav', 'mp3').

        Returns:
            str: Path to the converted audio file.
        """
        self.format = target_format  # Update the format dynamically if needed
        try:
            audio = self.load_audio(input_file)
            return self.save_audio(audio, output_file)
        except Exception as e:
            self.logger.error(f"Error converting {input_file} to {target_format}: {e}")
            raise
