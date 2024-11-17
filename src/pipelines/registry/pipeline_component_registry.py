# src/registry/pipeline_component_registry.py
from typing import Any
from src.registry.base_registry import BaseRegistry

class PipelineComponentRegistry(BaseRegistry[Any]):
    """
    A registry for managing components related to processing pipelines,
    such as processors, handlers, models, and batch processors.
    This class also incorporates specialized behavior from the original
    registries like PipelineRegistry and ProcessorRegistry, along with
    factory methods to instantiate batch processors.
    """
    def __init__(self):
        super().__init__()
        self._processors = {}
        self._handlers = {}
        self._batch_processors = {}
        self._batch_classes = {}

    # Processor methods
    def register_processor(self, name: str, processor):
        if name in self._processors:
            raise ValueError(f"Processor '{name}' is already registered.")
        self._processors[name] = processor

    def get_processor(self, name: str):
        if name not in self._processors:
            raise ValueError(f"Processor '{name}' not found in registry.")
        return self._processors[name]

    # Handler methods
    def register_handler(self, name: str, handler):
        if name in self._handlers:
            raise ValueError(f"Handler '{name}' is already registered.")
        self._handlers[name] = handler

    def get_handler(self, name: str):
        if name not in self._handlers:
            raise ValueError(f"Handler '{name}' not found in registry.")
        return self._handlers[name]

    # Batch Processor methods
    def register_batch_processor(self, name: str, batch_processor):
        if name in self._batch_processors:
            raise ValueError(f"Batch processor '{name}' is already registered.")
        self._batch_processors[name] = batch_processor

    def get_batch_processor(self, name: str):
        if name not in self._batch_processors:
            raise ValueError(f"Batch processor '{name}' not found in registry.")
        return self._batch_processors[name]

    def create_batch_processor(self, name: str, *args, **kwargs):
        """
        Create a new instance of a batch processor.

        Args:
            name (str): The name of the batch processor.
            *args, **kwargs: Additional arguments for initializing the batch processor.

        Returns:
            Any: An instance of the requested batch processor.
        """
        if name not in self._batch_processors:
            raise ValueError(f"Batch processor '{name}' not found in registry.")
        batch_processor_class = self._batch_processors[name]
        return batch_processor_class(*args, **kwargs)

    # Batch Class methods
    def register_batch_class(self, name: str, batch_class):
        if name in self._batch_classes:
            raise ValueError(f"Batch class '{name}' is already registered.")
        self._batch_classes[name] = batch_class

    def get_batch_class(self, name: str):
        if name not in self._batch_classes:
            raise ValueError(f"Batch class '{name}' not found in registry.")
        return self._batch_classes[name]

# Initialize the PipelineComponentRegistry
pipeline_component_registry = PipelineComponentRegistry()

# Register pipeline-related components
pipeline_component_registry.register_processor("audio_converter", AudioConverter)
pipeline_component_registry.register_processor("audio_transcriber", AudioTranscriber)
pipeline_component_registry.register_handler("audio_handler_normalize", NormalizeAudioHandler)
pipeline_component_registry.register_batch_processor("batch_processor_basic", BatchProcessor)
pipeline_component_registry.register_batch_class("batch_class_example", BatchRegistry)
pipeline_component_registry.register("transcription_saver", TranscriptionSaver)

# Example: Create an instance of a batch processor using the integrated factory method
batch_processor_instance = pipeline_component_registry.create_batch_processor("batch_processor_basic", config="example_config")
