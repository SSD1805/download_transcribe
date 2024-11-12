import os
import warnings
import soundfile as sf
from tqdm import tqdm
import whisperx
import whisper
import torch
from pydub import AudioSegment
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceManager

# Initialize the centralized logger and performance manager
log_manager = LoggerManager()
logger = log_manager.get_logger()

perf_manager = PerformanceManager()

# Suppress specific warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Paths for input modules files and output transcriptions
AUDIO_FILES_DIR = '/app/audio_files'
TRANSCRIPTIONS_DIR = '/app/transcriptions'

# Load WhisperX as the primary model and Whisper as the fallback
device = "cuda" if torch.cuda.is_available() else "cpu"
try:
    whisperx_model = whisperx.load_model("base", device)
    logger.info(f"WhisperX model loaded successfully on {device}.")
except Exception as e:
    logger.error(f"Failed to load WhisperX model: {e}")
    logger.info("Attempting to load standard Whisper as fallback.")
    try:
        whisper_model = whisper.load_model("base")
        logger.info("Standard Whisper model loaded successfully.")
    except Exception as fallback_e:
        logger.error(f"Failed to load Whisper model: {fallback_e}")
        exit(1)

# Function to sanitize file names
def sanitize_filename(title):
    return ''.join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in title)

# Function to convert modules files to WAV format
def convert_to_wav(audio_file):
    try:
        audio = AudioSegment.from_file(audio_file)
        wav_file = audio_file.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_file, format='wav')
        logger.info(f"Converted '{audio_file}' to WAV format.")
        return wav_file
    except Exception as e:
        logger.error(f"Error converting '{audio_file}' to WAV: {e}")
        return None

# Function to transcribe using WhisperX or Whisper as a fallback
def transcribe_audio(audio_file, use_whisperx=True):
    if use_whisperx:
        try:
            result = whisperx_model.transcribe(audio_file)
            logger.info(f"Transcription (WhisperX) completed for '{audio_file}'.")
            return result['segments']
        except Exception as e:
            logger.error(f"Error transcribing with WhisperX for '{audio_file}': {e}")
            logger.info("Falling back to standard Whisper.")
            use_whisperx = False

    # Fallback to standard Whisper
    if not use_whisperx:
        try:
            result = whisper_model.transcribe(audio_file)
            logger.info(f"Transcription (Whisper) completed for '{audio_file}'.")
            return [{'text': result['text']}]
        except Exception as e:
            logger.error(f"Error transcribing with Whisper for '{audio_file}': {e}")
            return []

# Main function to process and transcribe modules files
@perf_manager.track_performance
def transcribe_audio_files():
    os.makedirs(TRANSCRIPTIONS_DIR, exist_ok=True)
    audio_files = [f for f in os.listdir(AUDIO_FILES_DIR) if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]

    for file_name in tqdm(audio_files, desc="Transcribing modules files"):
        audio_file = os.path.join(AUDIO_FILES_DIR, file_name)
        sanitized_title = sanitize_filename(file_name.rsplit('.', 1)[0])
        transcription_file = os.path.join(TRANSCRIPTIONS_DIR, f'{sanitized_title}.txt')

        if os.path.exists(transcription_file):
            logger.info(f"Skipping '{file_name}' (already transcribed).")
            continue

        logger.info(f"Starting transcription for '{file_name}'...")

        # Convert to WAV if necessary
        if not file_name.endswith('.wav'):
            audio_file = convert_to_wav(audio_file)
            if not audio_file:
                logger.warning(f"Skipping '{file_name}' due to conversion error.")
                continue

        # Transcribe the modules and save the results
        segments = transcribe_audio(audio_file)
        try:
            with open(transcription_file, 'w') as f:
                for segment in segments:
                    f.write(f"{segment['text']}\n")
            logger.info(f"Transcription saved as '{transcription_file}'.")
        except Exception as e:
            logger.error(f"Error saving transcription for '{file_name}': {e}")

if __name__ == "__main__":
    perf_manager.monitor_memory_usage()  # Start monitoring memory usage
    transcribe_audio_files()
