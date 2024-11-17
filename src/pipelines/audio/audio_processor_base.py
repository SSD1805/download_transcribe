from abc import ABC, abstractmethod
from pydub import AudioSegment
import os
from typing import List

class AudioProcessorBase(ABC):
    """
    Abstract Base Class for all audio processors.
    Provides common methods for loading and saving audio.
    """
    def __init__(self, output_directory: str, format: str = 'wav'):
        self.output_directory = output_directory
        self.format = format
        os.makedirs(self.output_directory, exist_ok=True)

    def load_audio(self, input_file: str) -> AudioSegment:
        """
        Load an audio file.

        Args:
            input_file (str): Path to the input audio file.

        Returns:
            AudioSegment: The loaded audio segment.
        """
        try:
            return AudioSegment.from_file(input_file)
        except Exception as e:
            raise RuntimeError(f"Error loading audio file {input_file}: {e}")

    def save_audio(self, audio: AudioSegment, output_file: str) -> str:
        """
        Save an audio segment to a file.

        Args:
            audio (AudioSegment): The audio segment to save.
            output_file (str): The output file name.

        Returns:
            str: The path to the saved audio file.
        """
        output_path = os.path.join(self.output_directory, output_file)
        try:
            audio.export(output_path, format=self.format)
            return output_path
        except Exception as e:
            raise RuntimeError(f"Error saving audio file {output_file}: {e}")

    @abstractmethod
    def process(self, input_file: str, *args, **kwargs) -> str:
        """
        Abstract method for processing audio files. Must be implemented by subclasses.

        Args:
            input_file (str): Path to the input audio file.

        Returns:
            str: Path to the processed audio file.
        """
        pass


class AudioConverter(AudioProcessorBase):
    """
    Converts audio files to a specified format.
    """
    def process(self, input_file: str, output_file: str, target_format: str = 'wav') -> str:
        self.format = target_format
        audio = self.load_audio(input_file)
        return self.save_audio(audio, output_file)


class AudioNormalizer(AudioProcessorBase):
    """
    Normalizes audio to a standard volume level.
    """
    def process(self, input_file: str, output_file: str) -> str:
        from pydub import effects
        audio = self.load_audio(input_file)
        normalized_audio = effects.normalize(audio)
        return self.save_audio(normalized_audio, output_file)


class AudioSplitter(AudioProcessorBase):
    """
    Splits audio files into smaller chunks.
    """
    def process(self, input_file: str, chunk_duration_ms: int, output_file_prefix: str) -> List[str]:
        audio = self.load_audio(input_file)
        chunks = [audio[i:i + chunk_duration_ms] for i in range(0, len(audio), chunk_duration_ms)]
        chunk_files = []
        for idx, chunk in enumerate(chunks):
            chunk_file = f"{output_file_prefix}_chunk{idx}.{self.format}"
            chunk_files.append(self.save_audio(chunk, chunk_file))
        return chunk_files


class AudioTrimmer(AudioProcessorBase):
    """
    Trims silence from the beginning and end of an audio file.
    """
    def process(self, input_file: str, output_file: str, silence_thresh: int = -40) -> str:
        audio = self.load_audio(input_file)
        trimmed_audio = audio.strip_silence(silence_thresh=silence_thresh)
        return self.save_audio(trimmed_audio, output_file)
