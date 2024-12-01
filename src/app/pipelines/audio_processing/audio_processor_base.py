import os
from abc import ABC, abstractmethod

from pydub import AudioSegment


class AudioProcessorBase(ABC):
    def __init__(self, output_directory: str, logger, tracker=None, format: str = "wav"):
        self.output_directory = output_directory
        self.logger = logger
        self.tracker = tracker
        self.format = format
        os.makedirs(self.output_directory, exist_ok=True)

    def process_pipeline(self, input_file: str, output_file: str, *args, **kwargs):
        try:
            audio = self.load_audio(input_file)
            processed_audio = self.process(audio, *args, **kwargs)
            saved_file = self.save_audio(processed_audio, output_file)
            return saved_file
        except Exception as e:
            self.logger.error(f"Error processing file {input_file}: {e}")
            raise

    def load_audio(self, input_file: str) -> AudioSegment:
        if not input_file.strip():
            self.logger.error("Empty file path provided for loading audio.")
            raise ValueError("Empty file path is not allowed.")
        try:
            self.logger.info(f"Loading audio file: {input_file}")
            return AudioSegment.from_file(input_file)
        except Exception as e:
            self.logger.error(f"Failed to load audio file {input_file}: {e}")
            raise

    def save_audio(self, audio: AudioSegment, output_file: str) -> str:
        if not output_file.strip():
            self.logger.error("Empty file path provided for saving audio.")
            raise ValueError("Empty file path is not allowed.")
        output_path = os.path.join(self.output_directory, output_file)
        try:
            self.logger.info(f"Saving audio to {output_path}")
            audio.export(output_path, format=self.format)
            if self.tracker:
                self.tracker.track_execution("save_audio", {"file": output_path})
            return output_path
        except Exception as e:
            self.logger.error(f"Failed to save audio file {output_file}: {e}")
            raise

    @abstractmethod
    def process(self, audio: AudioSegment, *args, **kwargs) -> AudioSegment:
        pass
