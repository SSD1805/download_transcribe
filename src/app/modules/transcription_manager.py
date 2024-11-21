from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer

class ModelLoader:
    @inject
    def __init__(self,
                 logger=Provide[AppContainer.logger],
                 perf_tracker=Provide[AppContainer.performance_tracker],
                 model_registry=Provide[AppContainer.model_registry],
                 config_registry=Provide[AppContainer.configuration_registry]):
        """
        Initialize the ModelLoader.

        Args:
            logger: The logger instance from the AppContainer.
            perf_tracker: The performance tracker from the AppContainer.
            model_registry: The model registry for managing model instances.
            config_registry: Configuration registry for retrieving configurations.
        """
        self.logger = logger
        self.perf_tracker = perf_tracker
        self.model_registry = model_registry
        self.config_registry = config_registry

    @inject
    @perf_tracker.track
    def load_models(self):
        """
        Attempts to load WhisperX model first, with a fallback to standard Whisper model.

        Raises:
            ValueError: If both models fail to load.
        """
        try:
            # Load WhisperX model
            whisperx_model = self.model_registry.create_model("whisperx", "base")
            self.model_registry.register_model("whisperx", whisperx_model)
            self.logger.info("WhisperX model loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load WhisperX model: {e}")
            self.logger.info("Attempting to load standard Whisper model as a fallback.")
            self._load_fallback_whisper()

    @inject
    @perf_tracker.track
    def _load_fallback_whisper(self):
        """Attempts to load the standard Whisper model as a fallback."""
        try:
            # Load Whisper model
            whisper_model = self.model_registry.create_model("whisper", "base")
            self.model_registry.register_model("whisper", whisper_model)
            self.logger.info("Standard Whisper model loaded successfully.")
        except Exception as fallback_e:
            self.logger.error(f"Failed to load both WhisperX and Whisper models: {fallback_e}")
            raise ValueError("Could not load any transcription model") from fallback_e

    def transcribe_with_whisperx(self, audio_file, **kwargs):
        """
        Transcribe using WhisperX if it is loaded.

        Args:
            audio_file (str): Path to the audio file.
            **kwargs: Additional WhisperX parameters.

        Returns:
            dict: Transcription and alignment results.
        """
        whisperx_model = self.model_registry.get_model("whisperx")
        if not whisperx_model:
            raise ValueError("WhisperX model is not loaded.")
        try:
            self.logger.info(f"Transcribing with WhisperX: {audio_file}")
            result = whisperx_model.transcribe(audio_file, **kwargs)
            self.logger.info("WhisperX transcription completed.")
            return result
        except Exception as e:
            self.logger.error(f"Failed to transcribe with WhisperX: {e}")
            raise

    def transcribe_with_whisper(self, audio_file, **kwargs):
        """
        Transcribe using Whisper if it is loaded.

        Args:
            audio_file (str): Path to the audio file.
            **kwargs: Additional Whisper parameters.

        Returns:
            dict: Transcription results.
        """
        whisper_model = self.model_registry.get_model("whisper")
        if not whisper_model:
            raise ValueError("Whisper model is not loaded.")
        try:
            self.logger.info(f"Transcribing with Whisper: {audio_file}")
            result = whisper_model.transcribe(audio_file, **kwargs)
            self.logger.info("Whisper transcription completed.")
            return result
        except Exception as e:
            self.logger.error(f"Failed to transcribe with Whisper: {e}")
            raise


# Example usage
if __name__ == "__main__":

    container = AppContainer()
    container.wire(modules=[__name__])

    model_loader = ModelLoader()
    model_loader.load_models()

    # Example audio file path
    audio_file = "example_audio.wav"

    # Attempt transcription with WhisperX
    try:
        whisperx_result = model_loader.transcribe_with_whisperx(audio_file)
        model_loader.logger.info(f"WhisperX Result: {whisperx_result}")
    except ValueError as e:
        model_loader.logger.warning(f"WhisperX failed: {e}")

    # Attempt transcription with Whisper as fallback
    try:
        whisper_result = model_loader.transcribe_with_whisper(audio_file)
        model_loader.logger.info(f"Whisper Result: {whisper_result}")
    except ValueError as e:
        model_loader.logger.warning(f"Whisper failed: {e}")
