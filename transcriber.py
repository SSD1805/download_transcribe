import os
import whisper
import warnings
import json

# Suppress specific warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Paths for input audio files and output transcriptions
PODCAST_AUDIO_DIR = '/app/podcast_audio'
TRANSCRIPTIONS_DIR = '/app/transcriptions'

# Load the Whisper model, allowing configuration via environment variable
model_size = os.getenv("WHISPER_MODEL_SIZE", "base")  # Default to "base" if not set
try:
    whisper_model = whisper.load_model(model_size)
    print(f"Loaded Whisper model: {model_size}")
except Exception as e:
    print(f"Error loading Whisper model '{model_size}': {e}")
    whisper_model = whisper.load_model("base")  # Fallback to base model if the specified model fails

# Function to sanitize file names to prevent invalid characters in filenames
def sanitize_filename(title):
    return ''.join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in title)

# Function to save transcription in text or JSON format
def save_transcription(text, sanitized_title, format="txt"):
    os.makedirs(TRANSCRIPTIONS_DIR, exist_ok=True)
    file_path = os.path.join(TRANSCRIPTIONS_DIR, f"{sanitized_title}.{format}")

    try:
        if format == "txt":
            with open(file_path, 'w') as f:
                f.write(text)
        elif format == "json":
            with open(file_path, 'w') as f:
                json.dump({"transcription": text}, f)
        print(f"Transcription saved as '{file_path}'")
    except Exception as e:
        print(f"Failed to save transcription for '{sanitized_title}': {e}")

# Function to transcribe a single audio file
def transcribe_audio(audio_file, output_format="txt"):
    sanitized_title = sanitize_filename(os.path.basename(audio_file).rsplit('.', 1)[0])
    transcription_file = os.path.join(TRANSCRIPTIONS_DIR, f"{sanitized_title}.{output_format}")

    # Check if the transcription file already exists to avoid duplicates
    if os.path.exists(transcription_file):
        print(f"Skipping '{audio_file}' (already transcribed).")
        return

    try:
        print(f"Starting transcription for '{audio_file}'...")
        result = whisper_model.transcribe(audio_file)
        print(f"Preview for '{audio_file}': {result['text'][:100]}...")

        # Save the transcription
        save_transcription(result['text'], sanitized_title, output_format)
    except Exception as e:
        print(f"Error transcribing '{audio_file}': {e}")

# Function to transcribe all audio files in the podcast directory
def transcribe_audio_files(output_format="txt"):
    os.makedirs(TRANSCRIPTIONS_DIR, exist_ok=True)

    for file_name in os.listdir(PODCAST_AUDIO_DIR):
        if file_name.endswith(('.mp3', '.wav', '.m4a', '.flac')):
            audio_file = os.path.join(PODCAST_AUDIO_DIR, file_name)
            transcribe_audio(audio_file, output_format)

if __name__ == "__main__":
    # Set transcription output format from environment variable (default to txt)
    output_format = os.getenv("TRANSCRIPTION_FORMAT", "txt")
    transcribe_audio_files(output_format)
