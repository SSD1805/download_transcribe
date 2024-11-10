import os
import whisper
import warnings
import logging
from pydub import AudioSegment
import soundfile as sf
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename='/app/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

logging.info('Logging is configured correctly.')

# Suppress specific warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Paths for input audio files and output transcriptions
AUDIO_FILES_DIR = '/app/audio_files'
TRANSCRIPTIONS_DIR = '/app/transcriptions'

# Load the Whisper model
whisper_model = whisper.load_model("base")

# Function to sanitize file names
def sanitize_filename(title):
    return ''.join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in title)

# Function to convert audio files to WAV format
def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_file = audio_file.rsplit('.', 1)[0] + '.wav'
    audio.export(wav_file, format='wav')
    return wav_file

# Function to transcribe audio files and save transcripts
def transcribe_audio_files():
    os.makedirs(TRANSCRIPTIONS_DIR, exist_ok=True)
    audio_files = [f for f in os.listdir(AUDIO_FILES_DIR) if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]

    for file_name in tqdm(audio_files, desc="Transcribing audio files"):
        audio_file = os.path.join(AUDIO_FILES_DIR, file_name)
        sanitized_title = sanitize_filename(file_name.rsplit('.', 1)[0])
        transcription_file = os.path.join(TRANSCRIPTIONS_DIR, f'{sanitized_title}.txt')

        if os.path.exists(transcription_file):
            logging.info(f"Skipping '{file_name}' (already transcribed).")
            continue

        logging.info(f"Starting transcription for '{file_name}'...")

        # Convert to WAV if necessary
        if not file_name.endswith('.wav'):
            audio_file = convert_to_wav(audio_file)

        result = whisper_model.transcribe(audio_file)
        logging.info(f"Preview for '{file_name}': {result['text'][:100]}...")

        with open(transcription_file, 'w') as f:
            f.write(result['text'])

        logging.info(f"Transcription saved as '{transcription_file}'.")

if __name__ == "__main__":
    transcribe_audio_files()