import os
from abc import ABC, abstractmethod

from dependency_injector.wiring import Provide, inject
from pydub import AudioSegment

from src.infrastructure.app.app_container import AppContainer


class AudioProcessorBase(ABC):
    """
    Abstract Base Class for all audio processing tasks.
    Provides shared functionality for loading, saving, and managing audio files.
    """

    @inject
    def __init__(
        self,
        output_directory: str,
        format: str = "wav",
        logger=Provide[AppContainer.logger],
        tracker=Provide[AppContainer.performance_tracker],
    ):
        self.output_directory = output_directory
        self.format = format
        self.logger = logger
        self.tracker = tracker
        os.makedirs(self.output_directory, exist_ok=True)

    def load_audio(self, input_file: str) -> AudioSegment:
        """Load an audio file."""
        try:
            self.logger.info(f"Loading audio file: {input_file}")
            return AudioSegment.from_file(input_file)
        except Exception as e:
            self.logger.error(f"Failed to load audio file {input_file}: {e}")
            raise RuntimeError(f"Error loading audio file {input_file}: {e}")

    def save_audio(self, audio: AudioSegment, output_file: str) -> str:
        """Save an audio segment."""
        output_path = os.path.join(self.output_directory, output_file)
        try:
            self.logger.info(f"Saving audio to {output_path}")
            audio.export(output_path, format=self.format)
            self.tracker.track_execution("save_audio", {"file": output_path})
            return output_path
        except Exception as e:
            self.logger.error(f"Failed to save audio file {output_file}: {e}")
            raise RuntimeError(f"Error saving audio file {output_file}: {e}")

    @abstractmethod
    def process(self, input_file: str, *args, **kwargs) -> str:
        """Abstract method for processing audio files."""
        pass
