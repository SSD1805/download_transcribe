import whisperx
import whisper
import torch
from src.core.logger_manager import LoggerManager
from src.custom_exceptions import ConfigurationError

log_manager = LoggerManager()
logger = log_manager.get_logger()

device = "cuda" if torch.cuda.is_available() else "cpu"
whisperx_model, whisper_model = None, None

try:
    whisperx_model = whisperx.load_model("base", device)
    logger.info(f"WhisperX model loaded successfully on {device}.")
except Exception as e:
    logger.error(f"Failed to load WhisperX model: {e}")
    logger.info("Attempting to load standard Whisper as a fallback.")
    try:
        whisper_model = whisper.load_model("base")
        logger.info("Standard Whisper model loaded successfully.")
    except Exception as fallback_e:
        logger.error(f"Failed to load both WhisperX and Whisper models: {fallback_e}")
        raise ConfigurationError("Could not load any transcription model") from fallback_e
