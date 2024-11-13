import os
import re
import pandas as pd
from tqdm import tqdm
from logger_manager_test import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

# Function to sanitize file names for safe saving
def sanitize_filename(title):
    return ''.join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in title)

# Ensure directories exist before proceeding
def ensure_directories_exist(*directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

# Function to check if both the modules and transcription_service files already exist
def files_exist(title, podcast_audio_dir, transcriptions_dir):
    sanitized_title = sanitize_filename(title)
    audio_file = os.path.join(podcast_audio_dir, f'{sanitized_title}.mp3')
    transcription_file = os.path.join(transcriptions_dir, f'{sanitized_title}.txt')
    audio_exists = os.path.exists(audio_file)
    transcription_exists = os.path.exists(transcription_file)
    logger.info(f"Audio file exists: {audio_exists}, Transcription file exists: {transcription_exists}")
    return audio_exists, transcription_exists

# Function to list all files in a directory with progress tracking
def list_files_with_progress(directory):
    files = []
    for file in tqdm(os.listdir(directory), desc="Listing files"):
        files.append(file)
    logger.info(f"Listed {len(files)} files in directory: {directory}")
    return files

# Function to save file metadata to a CSV file
def save_file_metadata_to_csv(directory, output_csv):
    files = list_files_with_progress(directory)
    metadata = [{"file_name": file, "size": os.path.getsize(os.path.join(directory, file))} for file in files]
    df = pd.DataFrame(metadata)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    logger.info(f"Saved file metadata to CSV: {output_csv}")