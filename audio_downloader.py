import os
import time
import yt_dlp
import re
import logging
from retry import retry  # For retry logic on download failures

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment and Path Configurations
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
PODCAST_AUDIO_DIR = os.path.abspath('./podcast_audio')
COOKIE_PATH = r'C:\Users\share\Downloads\youtube.com_cookies.txt'

# Ensure the podcast_audio directory exists
if not os.path.exists(PODCAST_AUDIO_DIR):
    os.makedirs(PODCAST_AUDIO_DIR)
    logging.info(f"Directory '{PODCAST_AUDIO_DIR}' created.")
else:
    logging.info(f"Using existing directory '{PODCAST_AUDIO_DIR}'.")

# yt-dlp options with cookies and progress hooks
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(PODCAST_AUDIO_DIR, '%(title)s.%(ext)s'),
    'ignoreerrors': True,
    'ffmpeg_location': FFMPEG_PATH,
    'cookiefile': COOKIE_PATH,
}

# Progress hook function for yt-dlp
def progress_hook(d):
    if d['status'] == 'downloading':
        logging.info(f"Downloading {d.get('filename')} - {d.get('_percent_str')} complete")
    elif d['status'] == 'finished':
        logging.info(f"Download finished, now post-processing {d.get('filename')}")

ydl_opts['progress_hooks'] = [progress_hook]

# Retry mechanism decorator for downloading
@retry(tries=3, delay=5, backoff=2)
def download_audio(video_url):
    """Download audio from a YouTube video URL using yt-dlp."""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        logging.info(f"Starting download for {video_url}")
        try:
            ydl.download([video_url])
            logging.info(f"Download successful for {video_url}")
        except Exception as e:
            logging.error(f"Failed to download {video_url}: {e}")
            raise

# Sanitize filename to prevent issues with saving
def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', '_', title)

# Check if the audio file already exists based on yt-dlp's generated filename
def file_exists(video_info):
    title = video_info.get("title", "Unknown Title")
    sanitized_title = sanitize_filename(title)
    output_filename = os.path.join(PODCAST_AUDIO_DIR, f'{sanitized_title}.mp3')
    return os.path.isfile(output_filename)

# Handle downloading a single video and checking for existing files
def download_video(video_info):
    if video_info is None:
        logging.warning("Skipping video because it's unavailable.")
        return

    title = video_info.get("title", "Unknown Title")
    if file_exists(video_info):
        logging.info(f'Skipping {title} (already exists in podcast_audio)')
        return

    logging.info(f'Extracting and downloading audio for {title}')
    video_url = f'https://www.youtube.com/watch?v={video_info.get("id")}'
    download_audio(video_url)
    time.sleep(5)  # To avoid bot detection, wait briefly between downloads

# Download audio from a YouTube channel URL
def download_audio_from_channel(channel_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        video_entries = info_dict.get('entries', [])
        logging.info(f'Total videos found: {len(video_entries)}')

        for idx, video_info in enumerate(video_entries):
            logging.info(f'Processing video {idx + 1}/{len(video_entries)}...')
            download_video(video_info)

# Example usage
if __name__ == '__main__':
    channel_url = ''  # Add your YouTube channel URL here
    download_audio_from_channel(channel_url)
