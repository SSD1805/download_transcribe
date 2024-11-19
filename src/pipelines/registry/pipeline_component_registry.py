from typing import Any
from src.pipelines.registry.base_registry import BaseRegistry
from src.utils.structlog_logger import StructLogger

logger = StructLogger.get_logger()

class PipelineComponentRegistry(BaseRegistry[Any]):
    def __init__(self):
        super().__init__()
        self._processors = {}
        self._handlers = {}
        self._batch_processors = {}
        self._batch_classes = {}

    def register_processor(self, name: str, processor):
        if name in self._processors:
            raise ValueError(f"Processor '{name}' is already registered.")
        self._processors[name] = processor
        logger.info(f"Processor '{name}' registered.")

    def get_processor(self, name: str):
        if name not in self._processors:
            raise ValueError(f"Processor '{name}' not found in registry.")
        return self._processors[name]

    def register_handler(self, name: str, handler):
        if name in self._handlers:
            raise ValueError(f"Handler '{name}' is already registered.")
        self._handlers[name] = handler
        logger.info(f"Handler '{name}' registered.")

    def get_handler(self, name: str):
        if name not in self._handlers:
            raise ValueError(f"Handler '{name}' not found in registry.")
        return self._handlers[name]

    def register_batch_processor(self, name: str, batch_processor):
        if name in self._batch_processors:
            raise ValueError(f"Batch processor '{name}' is already registered.")
        self._batch_processors[name] = batch_processor
        logger.info(f"Batch processor '{name}' registered.")

    def get_batch_processor(self, name: str):
        if name not in self._batch_processors:
            raise ValueError(f"Batch processor '{name}' not found in registry.")
        return self._batch_processors[name]

    def create_batch_processor(self, name: str, *args, **kwargs):
        if name not in self._batch_processors:
            raise ValueError(f"Batch processor '{name}' not found in registry.")
        batch_processor_class = self._batch_processors[name]
        logger.info(f"Creating batch processor instance for '{name}'.")
        return batch_processor_class(*args, **kwargs)

# Initialize the PipelineComponentRegistry
pipeline_component_registry = PipelineComponentRegistry()
