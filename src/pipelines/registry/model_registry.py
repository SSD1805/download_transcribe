# src/registry/model_registry.py
from typing import Any, Type

class ModelRegistry:
    """
    A registry for managing different models used in the system, such as transcribers and NLP models.
    This includes both registering existing model instances and creating new model instances as needed.
    """
    def __init__(self):
        self._registered_models = {}
        self._model_factories = {}

    # Registration Methods
    def register_model(self, name: str, model: Any):
        """
        Register an existing model instance.
        """
        if name in self._registered_models:
            raise ValueError(f"Model '{name}' is already registered.")
        self._registered_models[name] = model

    def get_model(self, name: str) -> Any:
        """
        Retrieve a registered model instance by name.
        """
        if name not in self._registered_models:
            raise ValueError(f"Model '{name}' not found in registry.")
        return self._registered_models[name]

    # Factory Registration
    def register_model_factory(self, name: str, model_class: Type, *args, **kwargs):
        """
        Register a model factory that can be used to create new model instances.
        """
        if name in self._model_factories:
            raise ValueError(f"Model factory for '{name}' is already registered.")
        self._model_factories[name] = (model_class, args, kwargs)

    def create_model(self, name: str, *args, **kwargs) -> Any:
        """
        Create a new instance of a model using the registered factory.
        """
        if name not in self._model_factories:
            raise ValueError(f"Model factory for '{name}' not found in registry.")
        model_class, default_args, default_kwargs = self._model_factories[name]
        combined_args = default_args + args
        combined_kwargs = {**default_kwargs, **kwargs}
        return model_class(*combined_args, **combined_kwargs)

# Initialize the ModelRegistry
model_registry = ModelRegistry()

# Register pre-existing models
whisper_transcriber_instance = WhisperTranscriber()
model_registry.register_model("whisper_transcriber", whisper_transcriber_instance)

# Register model factories for dynamic creation
model_registry.register_model_factory("nlp_sentiment_model", SentimentAnalysisModel, param1="default_value")
model_registry.register_model_factory("language_detection_model", LanguageDetectionModel)

# Retrieve a registered model instance
retrieved_model = model_registry.get_model("whisper_transcriber")

# Create a new model instance using factory logic
new_sentiment_model = model_registry.create_model("nlp_sentiment_model", param2="custom_value")
