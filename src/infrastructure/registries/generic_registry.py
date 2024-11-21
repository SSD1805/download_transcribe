from typing import Callable, Dict, Union, TypeVar, Generic
from threading import Lock
from abc import ABC, abstractmethod
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer

# Define a generic type for the registries.
T = TypeVar('T')

class GenericRegistry(ABC, Generic[T]):
    """
    A reusable base class for registries with type safety, basic validation, thread safety,
    logging, and performance tracking.
    Handles common operations like adding, retrieving, and validating items.
    """
    @inject
    def __init__(self, logger=Provide[AppContainer.struct_logger], tracker=Provide[AppContainer.performance_tracker]):
        self._registry: Dict[str, Union[T, Callable[..., T]]] = {}
        self._lock = Lock()
        self.logger = logger
        self.tracker = tracker

    def register(self, name: str, item: Union[T, Callable[..., T]]):
        """
        Register an item with a unique name.

        Args:
            name (str): Unique name for the item.
            item (T or Callable[..., T]): The item or a callable to produce the item.
        """
        with self._lock:
            with self.tracker.track_execution("Register Item"):
                if name in self._registry:
                    self.logger.error(f"Item with name '{name}' is already registered.")
                    raise ValueError(f"Item with name '{name}' is already registered.")
                self._registry[name] = item
                self.logger.info(f"Registered item with name: '{name}'.")

    def get(self, name: str) -> Union[T, Callable[..., T]]:
        """
        Retrieve an item by name.

        Args:
            name (str): The name of the registered item.

        Returns:
            T or Callable[..., T]: The requested item or callable.
        """
        with self._lock:
            with self.tracker.track_execution("Get Item"):
                if name not in self._registry:
                    available = ", ".join(self._registry.keys())
                    self.logger.error(f"Item '{name}' is not registered. Available: {available}")
                    raise ValueError(f"Item '{name}' is not registered. Available: {available}")
                self.logger.info(f"Retrieved item with name: '{name}'.")
                return self._registry[name]

    def list_items(self) -> Dict[str, Union[T, Callable[..., T]]]:
        """
        List all registered items.

        Returns:
            Dict[str, T or Callable[..., T]]: A dictionary of all registered items.
        """
        with self._lock:
            with self.tracker.track_execution("List Items"):
                self.logger.info("Listing all registered items.")
                return self._registry

    @abstractmethod
    def validate_item(self, item: T) -> bool:
        """
        Hook method for child classes to implement custom validation.

        Args:
            item (T): The item to validate.

        Returns:
            bool: Whether the item is valid.
        """
        pass

# Example usage of the refactored GenericRegistry.
class RefactoredProcessorRegistry(GenericRegistry[Callable[[int], int]]):
    def validate_item(self, item: Callable[[int], int]) -> bool:
        # Example validation logic: check if item is callable
        if callable(item):
            self.logger.info("Validated processor item.")
            return True
        self.logger.error("Invalid processor item. It must be callable.")
        return False

# Reinitialize the processor registry.
processor_registry = RefactoredProcessorRegistry()

# Register a processor that takes one argument.
processor_registry.register("example_processor", lambda x: x * 2)

# Retrieve the registered processor without automatic invocation.
retrieved_processor = processor_registry.get("example_processor")
result = retrieved_processor(5)  # Invoke callable manually with correct argument.

print(result)  # Expected output: 10
