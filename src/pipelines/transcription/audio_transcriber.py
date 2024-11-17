import whisperx
import whisper
import torch
from src.core.services import CoreServices


class AudioTranscriber:
    def __init__(self, device=None):
        """
        Initialize the AudioTranscriber with the appropriate device and models.

        Args:
            device (str, optional): Device to use for inference ('cuda' or 'cpu').
                                    Defaults to 'cuda' if available, otherwise 'cpu'.
        """
        self.logger = CoreServices.get_logger()
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.whisperx_model = self._load_model(whisperx, "WhisperX")
        self.whisper_model = self._load_model(whisper, "Whisper")

    def _load_model(self, model_lib, model_name):
        try:
            model = model_lib.load_model("base", self.device)
            self.logger.info(f"{model_name} model loaded successfully on {self.device}.")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load {model_name} model: {e}")
            return None

    def transcribe(self, audio_file, use_whisperx=True):
        """
        Transcribe an audio file using WhisperX or Whisper as a fallback.

        Args:
            audio_file (str): Path to the audio file.
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
        try:
            result = model.transcribe(audio_file)
            self.logger.info(f"Transcription ({model_name}) completed for '{audio_file}'.")
            return result.get("segments", []) if model_name == "WhisperX" else [{"text": result.get("text", "")}]
        except Exception as e:
            self.logger.error(f"Error transcribing with {model_name} for '{audio_file}': {e}")
            return []
