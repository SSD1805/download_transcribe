from abc import ABC, abstractmethod

from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class TextProcessorBase(ABC):
    """
    Abstract base class for all text_processing processing components.
    Provides shared functionality and centralized dependency injection.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.struct_logger],
        tracker=Provide[AppContainer.performance_tracker],
    ):
        self.logger = logger
        self.tracker = tracker

    def validate_text(self, text: str) -> bool:
        """Validate input text_processing."""
        if not text or not isinstance(text, str):
            self.logger.warning("Invalid input text_processing provided.")
            return False
        return True

    @abstractmethod
    def process(self, text: str, *args, **kwargs):
        """
        Abstract method for processing text_processing. Must be implemented by subclasses.
        """
        pass
