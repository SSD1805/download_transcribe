import whisperx
import whisper
import torch
from src.pipelines.download.custom_exceptions import ConfigurationError
from src.core.services import CoreServices

# Get logger and performance tracker from CoreServices
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


class ModelLoader:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.whisperx_model = None
        self.whisper_model = None

    @perf_tracker.track  # Track performance of the model loading method
    def load_models(self):
        """
        Attempts to load WhisperX model first, with a fallback to standard Whisper model.

        Raises:
            ConfigurationError: If both models fail to load.
        """
        try:
            self.whisperx_model = whisperx.load_model("base", self.device)
            logger.info(f"WhisperX model loaded successfully on {self.device}.")
        except Exception as e:
            logger.error(f"Failed to load WhisperX model: {e}")
            logger.info("Attempting to load standard Whisper model as a fallback.")
            self._load_fallback_whisper()

    @perf_tracker.track  # Track performance of the fallback model loading method
    def _load_fallback_whisper(self):
        """Attempts to load the standard Whisper model as a fallback."""
        try:
            self.whisper_model = whisper.load_model("base")
            logger.info("Standard Whisper model loaded successfully.")
        except Exception as fallback_e:
            logger.error(f"Failed to load both WhisperX and Whisper models: {fallback_e}")
            raise ConfigurationError("Could not load any transcription model") from fallback_e


# Instantiate ModelLoader and attempt to load models
model_loader = ModelLoader()
model_loader.load_models()
