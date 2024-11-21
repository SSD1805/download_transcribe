from typing import Callable, Type, Dict
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer
from abc import ABC, abstractmethod

# Define an abstract PipelineComponent class for Composite Pattern
class PipelineComponent(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the pipeline component."""
        pass

class Processor(PipelineComponent):
    def __init__(self, processor_function: Callable):
        self.processor_function = processor_function

    def execute(self, *args, **kwargs):
        return self.processor_function(*args, **kwargs)

class Handler(PipelineComponent):
    def __init__(self, handler_function: Callable):
        self.handler_function = handler_function

    def execute(self, *args, **kwargs):
        return self.handler_function(*args, **kwargs)

class BatchProcessor(PipelineComponent):
    def __init__(self, batch_processor_class: Type, *args, **kwargs):
        self.batch_processor_instance = batch_processor_class(*args, **kwargs)

    def execute(self, *args, **kwargs):
        return self.batch_processor_instance.process(*args, **kwargs)

class CompositePipeline(PipelineComponent):
    def __init__(self):
        self._children: Dict[str, PipelineComponent] = {}

    def add(self, name: str, component: PipelineComponent):
        if name in self._children:
            raise ValueError(f"Component with name '{name}' is already added.")
        self._children[name] = component

    def remove(self, name: str):
        if name in self._children:
            del self._children[name]
        else:
            raise ValueError(f"Component with name '{name}' does not exist.")

    def execute(self, *args, **kwargs):
        results = {}
        for name, component in self._children.items():
            results[name] = component.execute(*args, **kwargs)
        return results

class PipelineRegistry:
    """
    A registry for managing different components used in the pipeline system,
    such as processors, handlers, and batch processors.
    """
    _instance = None

    @inject
    def __new__(cls, generic_registry=Provide[AppContainer.generic_registry], concurrency=Provide[AppContainer.concurrency_utilities]):
        if not cls._instance:
            with concurrency.get_lock():  # Use concurrency utility for thread safety
                if not cls._instance:
                    cls._instance = super(PipelineRegistry, cls).__new__(cls)
                    cls._instance._init_singleton(generic_registry, concurrency)
        return cls._instance

    @inject
    def _init_singleton(self, generic_registry, concurrency, logger=Provide[AppContainer.struct_logger], tracker=Provide[AppContainer.performance_tracker]):
        self.generic_registry = generic_registry
        self.concurrency = concurrency
        self.logger = logger
        self.tracker = tracker
        self._composite_pipeline = CompositePipeline()
        self.logger.info("Initialized PipelineRegistry singleton.")

    def validate_item(self, item: PipelineComponent) -> bool:
        """
        Validate if the item being registered is a valid PipelineComponent.

        Args:
            item (PipelineComponent): The pipeline component to validate.

        Returns:
            bool: Whether the pipeline component is valid.
        """
        if isinstance(item, PipelineComponent):
            self.logger.info("Validated pipeline component successfully.")
            return True
        else:
            self.logger.error("Invalid pipeline component. It must be an instance of PipelineComponent.")
            return False

    def register_processor(self, name: str, processor_function: Callable):
        """
        Register a processor for the pipeline.
        """
        processor = Processor(processor_function)
        with self.concurrency.get_lock():
            if self.validate_item(processor):
                self.generic_registry.add_item(name, processor)
                self.logger.info(f"Processor '{name}' registered successfully.")

    def register_handler(self, name: str, handler_function: Callable):
        """
        Register a handler for the pipeline.
        """
        handler = Handler(handler_function)
        with self.concurrency.get_lock():
            if self.validate_item(handler):
                self.generic_registry.add_item(name, handler)
                self.logger.info(f"Handler '{name}' registered successfully.")

    def register_batch_processor(self, name: str, batch_processor_class: Type, *args, **kwargs):
        """
        Register a batch processor class for the pipeline.
        """
        batch_processor = BatchProcessor(batch_processor_class, *args, **kwargs)
        with self.concurrency.get_lock():
            if self.validate_item(batch_processor):
                self.generic_registry.add_item(name, batch_processor)
                self.logger.info(f"Batch Processor '{name}' registered successfully.")

    def add_to_composite(self, name: str):
        """
        Add a registered component to the composite pipeline.
        """
        component = self.generic_registry.get_item(name)
        self._composite_pipeline.add(name, component)
        self.logger.info(f"Component '{name}' added to composite pipeline.")

    def execute_pipeline(self, *args, **kwargs):
        """
        Execute all components in the composite pipeline.
        """
        with self.concurrency.get_lock():
            with self.tracker.track_execution("Execute Composite Pipeline"):
                result = self._composite_pipeline.execute(*args, **kwargs)
                self.logger.info("Executed composite pipeline successfully.")
                return result

# Example Usage
if __name__ == "__main__":
    from src.infrastructure import container

    # Wire the AppContainer dependencies to this module
    container.wire(modules=[__name__])

    # Get the singleton instance of PipelineRegistry
    pipeline_registry = PipelineRegistry()

    # Register processors, handlers, and batch processors
    pipeline_registry.register_processor("example_processor", lambda x: x * 2)
    pipeline_registry.register_handler("example_handler", lambda x: f"Handled {x}")
    pipeline_registry.register_batch_processor("example_batch_processor", BatchProcessor, lambda x: [item * 2 for item in x])

    # Add components to the composite pipeline
    pipeline_registry.add_to_composite("example_processor")
    pipeline_registry.add_to_composite("example_handler")

    # Execute the entire composite pipeline
    pipeline_result = pipeline_registry.execute_pipeline(5)
    print(f"Pipeline Execution Result: {pipeline_result}")
