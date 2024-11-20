# Description: AudioTranscriber class to transcribe audio_processor files using WhisperX or Whisper.
import torch
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker


class AudioTranscriber:
    def __init__(self, device=None):
        """
        Initialize the AudioTranscriber with the appropriate device and models.

        Args:
            device (str, optional): Device to use for inference ('cuda' or 'cpu').
                                    Defaults to 'cuda' if available, otherwise 'cpu'.
        """
        self.logger = StructLogger.get_logger()
        self.performance_tracker = PerformanceTracker.get_instance()
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.whisperx_model = self._load_model("WhisperX")
        self.whisper_model = self._load_model("Whisper")

    def _load_model(self, model_name):
        """
        Dynamically load the transcription model based on its name.

        Args:
            model_name (str): Name of the model to load ("Whisper" or "WhisperX").

        Returns:
            model: Loaded model instance or None if loading fails.
        """
        try:
            with self.performance_tracker.track_execution(f"Load {model_name} Model"):
                if model_name == "Whisper" or model_name == "WhisperX":
                    import whisper  # Importing here to minimize unnecessary imports
                    model = whisper.load_model("base", self.device)
                    self.logger.info(f"{model_name} model loaded successfully on {self.device}.")
                    return model
        except Exception as e:
            self.logger.error(f"Failed to load {model_name} model: {e}")
        return None

    def transcribe(self, audio_file, use_whisperx=True):
        """
        Transcribe an audio_processor file using WhisperX or Whisper as a fallback.

        Args:
            audio_file (str): Path to the audio_processor file.
            use_whisperx (bool): Whether to attempt transcription with WhisperX first.

        Returns:
            list: A list of transcription segments or an empty list if transcription fails.
        """
        if use_whisperx and self.whisperx_model:
            return self._perform_transcription(self.whisperx_model, audio_file, "WhisperX")

        if self.whisper_model:
            return self._perform_transcription(self.whisper_model, audio_file, "Whisper")

        self.logger.error("No transcription models available.")
        return []

    def _perform_transcription(self, model, audio_file, model_name):
        """
        Perform transcription using the specified model.

        Args:
            model: Loaded transcription model.
            audio_file (str): Path to the audio_processor file.
            model_name (str): Name of the transcription model.

        Returns:
            list: Transcription segments or an empty list if transcription fails.
        """
        try:
            with self.performance_tracker.track_execution(f"Transcription with {model_name}"):
                result = model.transcribe(audio_file)
                self.logger.info(f"Transcription ({model_name}) completed for '{audio_file}'.")
                if model_name == "WhisperX":
                    return result.get("segments", [])
                return [{"text": result.get("text", "")}]
        except Exception as e:
            self.logger.error(f"Error transcribing with {model_name} for '{audio_file}': {e}")
            return []
