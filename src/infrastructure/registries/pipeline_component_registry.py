from typing import Any, Callable, Type
from threading import Lock
from src.infrastructure.registries.base_registry import BaseRegistry
from src.infrastructure.dependency_setup import container, di_inject, di_Provide

@di_inject
class PipelineComponentRegistry(BaseRegistry[Any]):
    def __init__(self, logger=di_Provide[container.logger]):
        super().__init__()
        self._processors = {}
        self._handlers = {}
        self._batch_processors = {}
        self._batch_classes = {}
        self._lock = Lock()  # Ensures thread safety
        self.logger = logger

    def _log_registration(self, component_type: str, name: str):
        """Log the successful registration of a component."""
        self.logger.info(f"{component_type} '{name}' registered successfully.")

    def _check_registration(self, component_type: str, name: str, registry: dict):
        """Check if a component is already registered."""
        with self._lock:
            if name in registry:
                self.logger.error(f"{component_type} '{name}' is already registered.")
                raise ValueError(f"{component_type} '{name}' is already registered.")

    def _get_component(self, component_type: str, name: str, registry: dict):
        """Retrieve a registered component from the registry."""
        with self._lock:
            if name not in registry:
                self.logger.error(f"{component_type} '{name}' not found in registry.")
                raise ValueError(f"{component_type} '{name}' not found in registry.")
            return registry[name]

    def register_processor(self, name: str, processor: Callable):
        """Register a processor for the pipeline."""
        self._check_registration("Processor", name, self._processors)
        with self._lock:
            self._processors[name] = processor
        self._log_registration("Processor", name)

    def get_processor(self, name: str) -> Callable:
        """Retrieve a registered processor."""
        return self._get_component("Processor", name, self._processors)

    def register_handler(self, name: str, handler: Callable):
        """Register a handler for the pipeline."""
        self._check_registration("Handler", name, self._handlers)
        with self._lock:
            self._handlers[name] = handler
        self._log_registration("Handler", name)

    def get_handler(self, name: str) -> Callable:
        """Retrieve a registered handler."""
        return self._get_component("Handler", name, self._handlers)

    def register_batch_processor(self, name: str, batch_processor: Type):
        """Register a batch processor class for the pipeline."""
        self._check_registration("Batch Processor", name, self._batch_processors)
        with self._lock:
            self._batch_processors[name] = batch_processor
        self._log_registration("Batch Processor", name)

    def get_batch_processor(self, name: str) -> Any:
        """Retrieve a registered batch processor class."""
        return self._get_component("Batch Processor", name, self._batch_processors)

    def create_batch_processor(self, name: str, *args, **kwargs) -> Any:
        """Create an instance of a registered batch processor."""
        batch_processor_class = self.get_batch_processor(name)
        self.logger.info(f"Creating batch processor instance for '{name}'.")
        return batch_processor_class(*args, **kwargs)

# Use AppContainer to create an instance of PipelineComponentRegistry
pipeline_component_registry = container.pipeline_component_registry()
