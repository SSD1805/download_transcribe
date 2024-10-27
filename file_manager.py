import os
import re
import logging

# Set up logging in file manager
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory paths for audio files and transcriptions
PODCAST_AUDIO_DIR = os.path.abspath('./podcast_audio')
TRANSCRIPTIONS_DIR = os.path.abspath('./transcriptions')

# Ensure the podcast and transcription directories exist
def ensure_directories_exist(*directories):
    """Ensure that all specified directories exist; create them if they don't."""
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Directory '{directory}' created.")
        else:
            logging.info(f"Using existing directory '{directory}'.")

# Sanitize filename by replacing invalid characters
def sanitize_filename(title):
    """Sanitize filenames by replacing invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', '_', title)

# Construct the full file path for a given audio or transcription file
def get_file_path(title, directory, extension="mp3"):
    """Construct the full file path for a given title within a specified directory."""
    sanitized_title = sanitize_filename(title)
    return os.path.join(directory, f"{sanitized_title}.{extension}")

# Check if audio and transcription files already exist for a given title
def files_exist(title):
    """Check if the audio file and transcription file exist for a given title."""
    audio_file_path = get_file_path(title, PODCAST_AUDIO_DIR, "mp3")
    transcription_file_path = get_file_path(title, TRANSCRIPTIONS_DIR, "txt")
    return os.path.exists(audio_file_path), os.path.exists(transcription_file_path)
