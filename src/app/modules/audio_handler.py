from abc import ABC, abstractmethod
from src.infrastructure import container, di_inject, di_Provide


# Base Command Class
class AudioCommand(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        """Method to execute the audio command."""
        pass


# Concrete Commands
class ConvertAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        target_format = kwargs.get('target_format')
        logger = kwargs.get('logger')
        logger.info(f"Converting {input_file} to {output_file} with format {target_format}")
        # Implement conversion logic here


class NormalizeAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        logger = kwargs.get('logger')
        logger.info(f"Normalizing {input_file} to {output_file}")
        # Implement normalization logic here


class SplitAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        chunk_duration_ms = kwargs.get('chunk_duration_ms')
        output_file_prefix = kwargs.get('output_file_prefix')
        logger = kwargs.get('logger')
        logger.info(f"Splitting {input_file} into chunks of {chunk_duration_ms} ms with prefix {output_file_prefix}")
        # Implement splitting logic here


class TrimAudioCommand(AudioCommand):
    def execute(self, **kwargs):
        input_file = kwargs.get('input_file')
        output_file = kwargs.get('output_file')
        silence_thresh = kwargs.get('silence_thresh')
        logger = kwargs.get('logger')
        logger.info(f"Trimming {input_file} with silence threshold {silence_thresh}")
        # Implement trimming logic here


# Handler Class
@di_inject
class AudioHandler:
    def __init__(
            self,
            handler_registry=di_Provide[container.pipeline_component_registry],
            logger=di_Provide[container.logger]
    ):
        self.handler_registry = handler_registry
        self.logger = logger

    def handle_audio(self, operation_name: str, **kwargs):
        try:
            # Retrieve the command from the registry
            command = self.handler_registry.get_processor(operation_name)
            if not isinstance(command, AudioCommand):
                raise ValueError(f"Registered command for operation '{operation_name}' is not a valid AudioCommand.")

            self.logger.info(f"Executing audio operation '{operation_name}'")

            # Add logger to kwargs so commands can use it
            kwargs['logger'] = self.logger
            command.execute(**kwargs)
        except ValueError as e:
            self.logger.error(f"Command for operation '{operation_name}' not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to execute command for operation '{operation_name}': {e}")
            raise
