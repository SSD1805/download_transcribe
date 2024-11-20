from typing import Any, Type
from threading import Lock
from src.infrastructure.dependency_setup import container, di_inject, di_Provide


class ModelRegistry:
    """
    A registry for managing different models used in the system, such as transcribers and NLP models.
    This includes both registering existing model instances and creating new model instances as needed.
    """

    @di_inject
    def __init__(self, logger=di_Provide[container.logger]):
        self._registered_models = {}
        self._model_factories = {}
        self._lock = Lock()  # Thread-safe lock for concurrent access
        self.logger = logger

    # Registration Methods
    def register_model(self, name: str, model: Any):
        """
        Register an existing model instance.

        Args:
            name (str): The name of the model.
            model (Any): The model instance to be registered.

        Raises:
            ValueError: If the model is already registered.
        """
        with self._lock:
            if name in self._registered_models:
                self.logger.error(f"Model '{name}' is already registered.")
                raise ValueError(f"Model '{name}' is already registered.")
            self._registered_models[name] = model
            self.logger.info(f"Model '{name}' registered successfully.")

    def get_model(self, name: str) -> Any:
        """
        Retrieve a registered model instance by name.

        Args:
            name (str): The name of the model to retrieve.

        Raises:
            ValueError: If the model is not registered.

        Returns:
            Any: The registered model instance.
        """
        with self._lock:
            if name not in self._registered_models:
                self.logger.error(f"Model '{name}' not found in registry.")
                raise ValueError(f"Model '{name}' not found in registry.")
            self.logger.info(f"Model '{name}' retrieved from registry.")
            return self._registered_models[name]

    # Factory Registration
    def register_model_factory(self, name: str, model_class: Type, *args, **kwargs):
        """
        Register a model factory that can be used to create new model instances.

        Args:
            name (str): The name of the model factory.
            model_class (Type): The class of the model to be instantiated.
            *args: Default positional arguments for the model class.
            **kwargs: Default keyword arguments for the model class.

        Raises:
            ValueError: If the model factory is already registered.
        """
        with self._lock:
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

        Raises:
            ValueError: If the model factory is not registered.

        Returns:
            Any: A new instance of the model.
        """
        with self._lock:
            if name not in self._model_factories:
                self.logger.error(f"Model factory for '{name}' not found in registry.")
                raise ValueError(f"Model factory for '{name}' not found in registry.")
            model_class, default_args, default_kwargs = self._model_factories[name]
            combined_args = default_args + args
            combined_kwargs = {**default_kwargs, **kwargs}
            model_instance = model_class(*combined_args, **combined_kwargs)
            self.logger.info(f"Model '{name}' instance created successfully.")
            return model_instance


# Initialize the ModelRegistry via Dependency Injection (if needed)
model_registry = container.model_registry()

# Example Usage

# Register pre-existing WhisperX model
from src.pipelines.transcription.whisperx_transcriber import WhisperXTranscriber
whisperx_transcriber_instance = WhisperXTranscriber()
model_registry.register_model("whisperx_transcriber", whisperx_transcriber_instance)

# Register model factories for dynamic creation (e.g., WhisperX if needed)
model_registry.register_model_factory("whisperx_transcriber_factory", WhisperXTranscriber)

# Register pre-existing models like Whisper
whisper_transcriber_instance = container.transcriber()  # Assuming transcriber is already provided in AppContainer
model_registry.register_model("whisper_transcriber", whisper_transcriber_instance)

# Register model factories for dynamic creation
model_registry.register_model_factory("nlp_sentiment_model", SentimentAnalysisModel, param1="default_value")
model_registry.register_model_factory("language_detection_model", LanguageDetectionModel)

# Retrieve a registered model instance
retrieved_model = model_registry.get_model("whisperx_transcriber")

# Create a new model instance using factory logic
new_sentiment_model = model_registry.create_model("nlp_sentiment_model", param2="custom_value")
