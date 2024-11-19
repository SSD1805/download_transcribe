import torch
import whisper
import whisperx
from src.pipelines.registry.error_registry import ConfigurationError
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

class ModelLoader:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.whisperx_model = None
        self.whisper_model = None

    @perf_tracker.track
    def load_models(self):
        """
        Attempts to load WhisperX model first, with a fallback to standard Whisper model.

        Raises:
            ConfigurationError: If both models fail to load.
        """
        try:
            # Load WhisperX model
            self.whisperx_model = whisperx.load_model("base", self.device)
            logger.info(f"WhisperX model loaded successfully on {self.device}.")
        except Exception as e:
            logger.error(f"Failed to load WhisperX model: {e}")
            logger.info("Attempting to load standard Whisper model as a fallback.")
            self._load_fallback_whisper()

    @perf_tracker.track
    def _load_fallback_whisper(self):
        """Attempts to load the standard Whisper model as a fallback."""
        try:
            # Load Whisper model
            self.whisper_model = whisper.load_model("base", self.device)
            logger.info("Standard Whisper model loaded successfully.")
        except Exception as fallback_e:
            logger.error(f"Failed to load both WhisperX and Whisper models: {fallback_e}")
            raise ConfigurationError("Could not load any transcription model") from fallback_e

    def transcribe_with_whisperx(self, audio_file, **kwargs):
        """
        Transcribe using WhisperX if it is loaded.

        Args:
            audio_file (str): Path to the audio file.
            **kwargs: Additional WhisperX parameters.

        Returns:
            dict: Transcription and alignment results.
        """
        if not self.whisperx_model:
            raise ConfigurationError("WhisperX model is not loaded.")
        try:
            logger.info(f"Transcribing with WhisperX: {audio_file}")
            result = self.whisperx_model.transcribe(audio_file, **kwargs)
            logger.info("WhisperX transcription completed.")
            return result
        except Exception as e:
            logger.error(f"Failed to transcribe with WhisperX: {e}")
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
        if not self.whisper_model:
            raise ConfigurationError("Whisper model is not loaded.")
        try:
            logger.info(f"Transcribing with Whisper: {audio_file}")
            result = self.whisper_model.transcribe(audio_file, **kwargs)
            logger.info("Whisper transcription completed.")
            return result
        except Exception as e:
            logger.error(f"Failed to transcribe with Whisper: {e}")
            raise


# Example usage
if __name__ == "__main__":
    model_loader = ModelLoader()
    model_loader.load_models()

    # Example audio file path
    audio_file = "example_audio.wav"

    # Attempt transcription with WhisperX
    try:
        whisperx_result = model_loader.transcribe_with_whisperx(audio_file)
        logger.info(f"WhisperX Result: {whisperx_result}")
    except ConfigurationError as e:
        logger.warning(f"WhisperX failed: {e}")

    # Attempt transcription with Whisper as fallback
    try:
        whisper_result = model_loader.transcribe_with_whisper(audio_file)
        logger.info(f"Whisper Result: {whisper_result}")
    except ConfigurationError as e:
        logger.warning(f"Whisper failed: {e}")
