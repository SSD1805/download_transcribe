from abc import ABC, abstractmethod
from src.pipelines.registry.preconfigured_audio_handler_registry import PreConfiguredAudioHandlerRegistry
from src.utils.logger_service import LoggerService

# Base Command Class
class AudioCommand(ABC):
    """
    Abstract base class representing an audio command.
    """
    @abstractmethod
    def execute(self, **kwargs):
        pass

# Concrete Commands
class ConvertAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        target_format = kwargs.get('target_format')
        logger = LoggerService.get_instance()
        logger.info(f"Converting {input_file} to {output_file} with format {target_format}")
        # Implement conversion logic here

class NormalizeAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        logger = LoggerService.get_instance()
        logger.info(f"Normalizing {input_file} to {output_file}")
        # Implement normalization logic here

class SplitAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        chunk_duration_ms = kwargs.get('chunk_duration_ms')
        output_file_prefix = kwargs.get('output_file_prefix')
        logger = LoggerService.get_instance()
        logger.info(f"Splitting {input_file} into chunks of {chunk_duration_ms} ms with prefix {output_file_prefix}")
        # Implement splitting logic here

class TrimAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        silence_thresh = kwargs.get('silence_thresh')
        logger = LoggerService.get_instance()
        logger.info(f"Trimming {input_file} with silence threshold {silence_thresh}")
        # Implement trimming logic here

# Handler Class
class AudioHandler:
    """
    Audio handler that uses a registry to retrieve and execute audio commands.
    """
    def __init__(self, handler_registry: PreConfiguredAudioHandlerRegistry):
        self.handler_registry = handler_registry
        self.logger = LoggerService.get_instance()

    def handle_audio(self, operation_name: str, **kwargs):
        """
        Handle an audio operation by delegating to the appropriate command.

        Args:
            operation_name (str): The operation to perform (e.g., 'convert', 'normalize').
            **kwargs: Arguments required by the command.
        """
        try:
            command = self.handler_registry.get(operation_name)
            self.logger.info(f"Executing audio operation '{operation_name}'")
            command.execute(**kwargs)
        except ValueError as e:
            self.logger.error(f"Command for operation '{operation_name}' not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to execute command for operation '{operation_name}': {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Assuming handler_registry is already configured with commands
    handler_registry = PreConfiguredAudioHandlerRegistry()
    handler_registry.register("convert", ConvertAudioCommand())
    handler_registry.register("normalize", NormalizeAudioCommand())
    handler_registry.register("split", SplitAudioCommand())
    handler_registry.register("trim", TrimAudioCommand())

    audio_handler = AudioHandler(handler_registry)

    # Convert audio
    audio_handler.handle_audio("convert", input_file="input.mp3", output_file="output.wav", target_format="wav")

    # Normalize audio
    audio_handler.handle_audio("normalize", input_file="input.wav", output_file="normalized.wav")

    # Split audio
    audio_handler.handle_audio("split", input_file="input.wav", chunk_duration_ms=30000, output_file_prefix="chunk_")

    # Trim audio
    audio_handler.handle_audio("trim", input_file="input.wav", output_file="trimmed.wav", silence_thresh=-40)
