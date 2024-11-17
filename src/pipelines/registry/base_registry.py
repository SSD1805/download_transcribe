from typing import Type, Callable, Dict, Any, Union, TypeVar, Generic

# Define a generic type for the registry.
T = TypeVar('T')

class BaseRegistry(Generic[T]):
    """
    A reusable base class for registries with type safety and basic validation.
    """
    def __init__(self):
        self._registry: Dict[str, Union[T, Callable[..., T]]] = {}

    def register(self, name: str, item: Union[T, Callable[..., T]]):
        """
        Register an item with a unique name.

        Args:
            name (str): Unique name for the item.
            item (T or Callable[..., T]): The item or a callable to produce the item.
        """
        if name in self._registry:
            raise ValueError(f"Item with name '{name}' is already registered.")
        self._registry[name] = item

    def get(self, name: str) -> Union[T, Callable[..., T]]:
        """
        Retrieve an item by name.

        Args:
            name (str): The name of the registered item.

        Returns:
            T or Callable[..., T]: The requested item or callable.
        """
        if name not in self._registry:
            available = ", ".join(self._registry.keys())
            raise ValueError(f"Item '{name}' is not registered. Available: {available}")
        return self._registry[name]

# Example usage of the refactored BaseRegistry.
class RefactoredProcessorRegistry(BaseRegistry[Callable[[int], int]]):
    pass

# Reinitialize the processor registry.
processor_registry = RefactoredProcessorRegistry()

# Register a processor that takes one argument.
processor_registry.register("example_processor", lambda x: x * 2)

# Retrieve the registered processor without automatic invocation.
retrieved_processor = processor_registry.get("example_processor")
result = retrieved_processor(5)  # Invoke callable manually with correct argument.

print(result)  # Expected output: 10
