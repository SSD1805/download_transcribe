import whisperx
import whisper
import torch
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

# Initialize logger and performance tracker
logger = LoggerManager().get_logger()
perf_tracker = PerformanceTracker()

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

    @perf_tracker.track  # Track the performance of the transcription method
    def transcribe(self, audio_file, use_whisperx=True):
        """
        Transcribe the audio file using WhisperX if available, otherwise fallback to Whisper.

        Args:
            audio_file (str): Path to the audio file.
            use_whisperx (bool): Whether to attempt transcription with WhisperX first.

        Returns:
            list: A list of transcription segments or an empty list if transcription fails.
        """
        if use_whisperx and self.whisperx_model:
            try:
                result = self.whisperx_model.transcribe(audio_file)
                logger.info(f"Transcription (WhisperX) completed for '{audio_file}'.")
                return result['segments']
            except Exception as e:
                logger.error(f"Error transcribing with WhisperX for '{audio_file}': {e}")

        # Fallback to standard Whisper if WhisperX is unavailable or fails
        if self.whisper_model:
            try:
                result = self.whisper_model.transcribe(audio_file)
                logger.info(f"Transcription (Whisper) completed for '{audio_file}'.")
                return [{'text': result['text']}]
            except Exception as e:
                logger.error(f"Error transcribing with Whisper for '{audio_file}': {e}")

        # Return an empty list if both transcription attempts fail
        return []
