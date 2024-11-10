import os
import time
import yt_dlp
import re
import logging
import pandas as pd
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename='/app/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

logging.info('Logging is configured correctly.')

# Directory where audio files will be saved (use an absolute path)
AUDIO_FILES_DIR = os.path.abspath('../../app/podcast_audio')

# Ensure the podcast_audio directory exists and use it
if not os.path.exists(AUDIO_FILES_DIR):
    os.makedirs(AUDIO_FILES_DIR)
    logging.info(f"Directory '{AUDIO_FILES_DIR}' created.")
else:
    logging.info(f"Using existing directory '{AUDIO_FILES_DIR}'.")

# yt-dlp options with cookies and ignoring errors
ydl_opts = {
    'format': 'bestaudio/best',  # Extract the best audio quality
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',  # Extract the audio using FFmpeg
        'preferredcodec': 'mp3',  # Convert to mp3
        'preferredquality': '192',  # Set the quality
    }],
    # Save files to podcast_audio folder (absolute path)
    'outtmpl': os.path.join(AUDIO_FILES_DIR, '%(title)s.%(ext)s'),
    'ignoreerrors': True,  # Skip videos that are unavailable or private
    'ffmpeg_location': r'C:\Program Files\ffmpeg-2024-09-19-git-0d5b68c27c-essentials_build\bin',  # ffmpeg_location
    'cookiefile': r'C:\Users\share\Downloads\youtube.com_cookies.txt',  # Path to the cookies.txt file
}

# Function to sanitize file names (the same way yt-dlp does)
def sanitize_filename(title):
    # Replace invalid characters with underscores or remove them
    return re.sub(r'[\\/*?:"<>|]', '_', title)

# Function to check if the audio file already exists based on yt-dlp's generated filename
def file_exists(video_info):
    # Get the title from the video_info
    title = video_info.get("title", "Unknown Title")

    # Sanitize the title
    sanitized_title = sanitize_filename(title)

    # Construct the filename manually based on the outtmpl
    output_filename = os.path.join(AUDIO_FILES_DIR, f'{sanitized_title}.mp3')

    # Check if the file exists in the podcast_audio directory
    return os.path.isfile(output_filename)

# Function to handle downloading a single video
def download_video(video_info):
    if video_info is None:
        logging.info("Skipping video because it's unavailable.")
        return

    title = video_info.get("title", "Unknown Title")

    # Check if the file already exists based on the generated filename
    if file_exists(video_info):
        logging.info(f'Skipping {title} (already exists in podcast_audio)')
        return

    # Download the video
    logging.info(f'Extracting and downloading audio for {title}')
    video_url = f'https://www.youtube.com/watch?v={video_info.get("id")}'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Sleep for 5 seconds between downloads to avoid bot detection
    time.sleep(5)

# Function to download audio from a YouTube channel URL
def download_audio_from_channel(channel_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Fetch metadata for all videos in the channel
        info_dict = ydl.extract_info(channel_url, download=False)

        # Process each video entry
        video_entries = info_dict.get('entries', [])
        logging.info(f'Total videos found: {len(video_entries)}')

        # Download each video with progress tracking
        for idx, video_info in enumerate(tqdm(video_entries, desc="Downloading videos")):
            logging.info(f'Processing video {idx + 1}/{len(video_entries)}...')
            download_video(video_info)

# Example usage
if __name__ == '__main__':
    # The channel URL
    channel_url = 'https://www.youtube.com/watch?v=cw22rBW4gFE&list=PLArKB4hKFyGEXDFY2N8bxfiJQtrmCwMDh'

    # Download all videos from the channel
    download_audio_from_channel(channel_url)