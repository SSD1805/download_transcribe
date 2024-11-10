import os
import time
import pandas as pd
import nltk
from tqdm import tqdm
from audio_downloader import download_audio_from_channel, download_audio
from transcriber import transcribe_audio
from app.file_manager import ensure_directories_exist, files_exist, sanitize_filename

# Download NLTK data
nltk.download('punkt')

# Set up directories
AUDIO_FILES_DIR = 'app/audio_files'
TRANSCRIPTIONS_DIR = 'app/transcriptions'
ensure_directories_exist(AUDIO_FILES_DIR, TRANSCRIPTIONS_DIR)

# Function to download and transcribe each video in a channel
def download_and_transcribe(channel_url):
    # Get video entries from the channel
    video_entries = download_audio_from_channel(channel_url)

    for idx, video_info in enumerate(tqdm(video_entries, desc="Processing videos")):
        title = video_info.get('title', 'Unknown Title')
        sanitized_title = sanitize_filename(title)

        audio_exists, transcription_exists = files_exist(sanitized_title, AUDIO_FILES_DIR, TRANSCRIPTIONS_DIR)

        if audio_exists and transcription_exists:
            print(f"Skipping {title} (already downloaded and transcribed)")
            continue

        if not audio_exists:
            print(f"Downloading {title}...")
            video_url = f"https://www.youtube.com/watch?v={video_info['id']}"
            download_audio(video_url)
            time.sleep(10)  # Avoid bot detection

        audio_file = os.path.join(AUDIO_FILES_DIR, f"{sanitized_title}.mp3")

        if not transcription_exists:
            transcribe_audio(audio_file, sanitized_title, TRANSCRIPTIONS_DIR)

if __name__ == "__main__":
    # Example usage
    channel_url = 'https://www.youtube.com/@refidao/videos'
    download_and_transcribe(channel_url)