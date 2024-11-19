from abc import ABC, abstractmethod
from src.infrastructure.registries import PreConfiguredAudioHandlerRegistry
from src.utils.structlog_logger import StructLogger

logger = StructLogger.get_logger()

# Base Command Class
class AudioCommand(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

# Concrete Commands
class ConvertAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        target_format = kwargs.get('target_format')
        logger.info(f"Converting {input_file} to {output_file} with format {target_format}")
        # Implement conversion logic here

class NormalizeAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        logger.info(f"Normalizing {input_file} to {output_file}")
        # Implement normalization logic here

class SplitAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        chunk_duration_ms = kwargs.get('chunk_duration_ms')
        output_file_prefix = kwargs.get('output_file_prefix')
        logger.info(f"Splitting {input_file} into chunks of {chunk_duration_ms} ms with prefix {output_file_prefix}")
        # Implement splitting logic here

class TrimAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        silence_thresh = kwargs.get('silence_thresh')
        logger.info(f"Trimming {input_file} with silence threshold {silence_thresh}")
        # Implement trimming logic here

# Handler Class
class AudioHandler:
    def __init__(self, handler_registry: PreConfiguredAudioHandlerRegistry):
        self.handler_registry = handler_registry

    def handle_audio(self, operation_name: str, **kwargs):
        try:
            command = self.handler_registry.get(operation_name)
            logger.info(f"Executing audio operation '{operation_name}'")
            command.execute(**kwargs)
        except ValueError as e:
            logger.error(f"Command for operation '{operation_name}' not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to execute command for operation '{operation_name}': {e}")
            raise
