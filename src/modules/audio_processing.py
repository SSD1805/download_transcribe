import os
from pydub import AudioSegment, effects
from logger import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

class AudioProcessor:
    def __init__(self, input_directory='app/audio_files', output_directory='app/processed_audio', format='wav'):
        self.input_directory = input_directory  # Directory for input audio files
        self.output_directory = output_directory  # Directory for processed audio files
        self.format = format  # Default output audio format
        os.makedirs(self.output_directory, exist_ok=True)  # Ensure the output directory exists

    def convert_audio_format(self, input_file, output_format=None):
        """
        Converts an audio file to the specified format.
        Args:
            input_file (str): Path to the input audio file.
            output_format (str, optional): Format to convert the audio file to. Defaults to class attribute 'format'.
        """
        output_format = output_format or self.format
        try:
            audio = AudioSegment.from_file(input_file)
            output_file = os.path.join(self.output_directory,
                                       f"{os.path.splitext(os.path.basename(input_file))[0]}.{output_format}")
            audio.export(output_file, format=output_format)
            logger.info(f"Converted {input_file} to {output_format} format.")
            return output_file
        except Exception as e:
            logger.error(f"Error converting {input_file}: {e}")
            return None

    def split_audio(self, input_file, segment_duration=30000):
        """
        Splits an audio file into smaller segments.
        Args:
            input_file (str): Path to the input audio file.
            segment_duration (int): Duration of each segment in milliseconds.
        """
        try:
            audio = AudioSegment.from_file(input_file)
            segments = []
            for i in range(0, len(audio), segment_duration):
                segment = audio[i:i + segment_duration]
                segment_file = os.path.join(self.output_directory,
                                            f"{os.path.splitext(os.path.basename(input_file))[0]}_part_{i // segment_duration}.{self.format}")
                segment.export(segment_file, format=self.format)
                segments.append(segment_file)
                logger.info(f"Segmented audio saved as {segment_file}")
            return segments
        except Exception as e:
            logger.error(f"Error splitting {input_file}: {e}")
            return []

    def normalize_audio(self, input_file):
        """
        Normalizes the volume of an audio file.
        """
        try:
            audio = AudioSegment.from_file(input_file)
            normalized_audio = effects.normalize(audio)
            output_file = os.path.join(self.output_directory,
                                       f"{os.path.splitext(os.path.basename(input_file))[0]}_normalized.{self.format}")
            normalized_audio.export(output_file, format=self.format)
            logger.info(f"Normalized audio saved as {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error normalizing {input_file}: {e}")
            return None

    def trim_silence(self, input_file):
        """
        Trims leading and trailing silence from an audio file.
        """
        try:
            audio = AudioSegment.from_file(input_file)
            trimmed_audio = audio.strip_silence(silence_thresh=audio.dBFS - 16)
            output_file = os.path.join(self.output_directory,
                                       f"{os.path.splitext(os.path.basename(input_file))[0]}_trimmed.{self.format}")
            trimmed_audio.export(output_file, format=self.format)
            logger.info(f"Trimmed audio saved as {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error trimming silence from {input_file}: {e}")
            return None