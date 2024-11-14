import whisperx
import whisper
import torch
from src.core.logger_manager import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

class AudioTranscriber:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.whisperx_model = self._load_whisperx_model()
        self.whisper_model = self._load_whisper_model()

    def _load_whisperx_model(self):
        try:
            model = whisperx.load_model("base", self.device)
            logger.info(f"WhisperX model loaded successfully on {self.device}.")
            return model
        except Exception as e:
            logger.error(f"Failed to load WhisperX model: {e}")
            return None

    def _load_whisper_model(self):
        try:
            model = whisper.load_model("base")
            logger.info("Standard Whisper model loaded successfully.")
            return model
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            return None

    def transcribe(self, audio_file, use_whisperx=True):
        if use_whisperx and self.whisperx_model:
            try:
                result = self.whisperx_model.transcribe(audio_file)
                logger.info(f"Transcription (WhisperX) completed for '{audio_file}'.")
                return result['segments']
            except Exception as e:
                logger.error(f"Error transcribing with WhisperX for '{audio_file}': {e}")

        # Fallback to standard Whisper
        if self.whisper_model:
            try:
                result = self.whisper_model.transcribe(audio_file)
                logger.info(f"Transcription (Whisper) completed for '{audio_file}'.")
                return [{'text': result['text']}]
            except Exception as e:
                logger.error(f"Error transcribing with Whisper for '{audio_file}': {e}")

        return []
