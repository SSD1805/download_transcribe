from typing import Any, Type, Callable, Dict
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer
from infrastructure.registries.generic_registry import GenericRegistry


class ModelRegistry(GenericRegistry[Any]):
    """
    A registry for managing different models used in the system, such as transcribers and NLP models.
    This includes both registering existing model instances and creating new model instances as needed.
    """
    _instance = None

    @inject
    def __new__(cls, base_registry=Provide[AppContainer.generic_registry], concurrency=Provide[AppContainer.concurrency_utilities]):
        if not cls._instance:
            with concurrency.get_lock():  # Use concurrency utility for thread safety
                if not cls._instance:
                    cls._instance = super(ModelRegistry, cls).__new__(cls)
                    cls._instance._init_singleton(base_registry, concurrency)
        return cls._instance

    @inject
    def _init_singleton(self, base_registry, concurrency, logger=Provide[AppContainer.struct_logger], tracker=Provide[AppContainer.performance_tracker]):
        super().__init__(logger, tracker)
        self.base_registry = base_registry
        self.concurrency = concurrency
        self._registered_models: Dict[str, Any] = {}
        self._model_factories: Dict[str, Callable] = {}
        self.logger.info("Initialized ModelRegistry singleton.")

    def validate_item(self, item: Any) -> bool:
        """
        Validate if the item being registered is a valid ML model.
        For this example, we check if the item has a 'predict' method, commonly found in ML models.

        Args:
            item (Any): The model instance to validate.

        Returns:
            bool: Whether the model instance is valid.
        """
        if hasattr(item, 'predict') and callable(getattr(item, 'predict')):
            self.logger.info("Validated model item successfully.")
            return True
        else:
            self.logger.error("Invalid model item. It must have a callable 'predict' method.")
            return False

    def register_model(self, name: str, model: Any):
        """
        Register an existing model instance.

        Args:
            name (str): The name of the model.
            model (Any): The model instance to be registered.
        """
        with self.concurrency.get_lock():
            with self.tracker.track_execution("Register Model"):
                if self.validate_item(model):
                    self._registered_models[name] = model
                    self.logger.info(f"Model '{name}' registered successfully.")
                else:
                    raise ValueError(f"Model '{name}' is not valid and cannot be registered.")

    def get_model(self, name: str) -> Any:
        """
        Retrieve a registered model instance by name.

        Args:
            name (str): The name of the model to retrieve.

        Returns:
            Any: The registered model instance.
        """
        with self.concurrency.get_lock():
            with self.tracker.track_execution("Get Model"):
                if name not in self._registered_models:
                    self.logger.error(f"Model '{name}' not found in registry.")
                    raise ValueError(f"Model '{name}' not found in registry.")
                self.logger.info(f"Model '{name}' retrieved from registry.")
                return self._registered_models[name]

    def register_model_factory(self, name: str, model_class: Type, *args, **kwargs):
        """
        Register a model factory that can be used to create new model instances.

        Args:
            name (str): The name of the model factory.
            model_class (Type): The class of the model to be instantiated.
            *args: Default positional arguments for the model class.
            **kwargs: Default keyword arguments for the model class.
        """
        with self.concurrency.get_lock():
            with self.tracker.track_execution("Register Model Factory"):
                if name in self._model_factories:
                    self.logger.error(f"Model factory for '{name}' is already registered.")
                    raise ValueError(f"Model factory for '{name}' is already registered.")
                self._model_factories[name] = (model_class, args, kwargs)
                self.logger.info(f"Model factory for '{name}' registered successfully.")

    def create_model(self, name: str, *args, **kwargs) -> Any:
        """
        Create a new instance of a model using the registered factory.

        Args:
            name (str): The name of the model factory to use.
            *args: Additional positional arguments for the model class.
            **kwargs: Additional keyword arguments for the model class.

        Returns:
            Any: A new instance of the model.
        """
        with self.concurrency.get_lock():
            with self.tracker.track_execution("Create Model"):
                if name not in self._model_factories:
                    self.logger.error(f"Model factory for '{name}' not found in registry.")
                    raise ValueError(f"Model factory for '{name}' not found in registry.")
                model_class, default_args, default_kwargs = self._model_factories[name]
                combined_args = default_args + args
                combined_kwargs = {**default_kwargs, **kwargs}
                model_instance = model_class(*combined_args, **combined_kwargs)
                self.logger.info(f"Model '{name}' instance created successfully.")
                return model_instance

# Example Usage
if __name__ == "__main__":
    from infrastructure.dependency_setup import container

    # Wire the AppContainer dependencies to this module
    container.wire(modules=[__name__])

    # Get the singleton instance of ModelRegistry
    model_registry = ModelRegistry()

    # Register an existing WhisperX model
    from src.pipelines.transcription.whisperx_transcriber import WhisperXTranscriber
    whisperx_transcriber_instance = WhisperXTranscriber()
    model_registry.register_model("whisperx_transcriber", whisperx_transcriber_instance)

    # Register a model factory for dynamic creation
    model_registry.register_model_factory("whisperx_transcriber_factory", WhisperXTranscriber)

    # Retrieve a registered model instance
    retrieved_model = model_registry.get_model("whisperx_transcriber")

    # Create a new model instance using factory logic
    new_sentiment_model = model_registry.create_model("whisperx_transcriber_factory")
