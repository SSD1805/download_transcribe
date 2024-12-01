from abc import ABC, abstractmethod  # Standard library

from dependency_injector.wiring import Provide, inject  # Third-party libraries

from src.infrastructure.app.app_container import AppContainer  # Local imports


# Base Command Class
class AudioCommand(ABC):
    """
    Abstract base class for all audio commands.
    """

    @abstractmethod
    def execute(self, **kwargs):
        """
        Method to execute the audio command.
        Must be implemented by concrete classes.
        """
        pass


@inject
class AudioHandler:
    """
    Handles execution of audio operations by dispatching to registered commands.
    """

    def __init__(
        self,
        handler_registry=Provide[AppContainer.pipeline_component_registry],
        logger=Provide[AppContainer.logger],
    ):
        self.handler_registry = handler_registry
        self.logger = logger

    def handle_audio(self, operation_name: str, **kwargs):
        """
        Handles the execution of audio operations by dispatching
        to the appropriate command.

        Args:
            operation_name (str): The name of the operation to execute.
            **kwargs: Additional arguments to pass to the command.
        """
        try:
            # Retrieve the command from the registry
            command = self.handler_registry.get_processor(operation_name)
            if not isinstance(command, AudioCommand):
                self.logger.error(
                    f"Registered command for operation '{operation_name}' "
                    f"is not valid."
                )
                raise ValueError(
                    f"Registered command for operation '{operation_name}' "
                    f"is not a valid AudioCommand."
                )

            self.logger.info(f"Executing audio operation '{operation_name}'")

            # Add logger to kwargs for use in the command
            kwargs["logger"] = self.logger
            command.execute(**kwargs)
        except ValueError as ve:
            self.logger.error(
                f"ValueError encountered while handling operation "
                f"'{operation_name}': {ve}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error during operation '{operation_name}': {e}"
            )
            raise
