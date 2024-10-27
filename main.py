from audio_downloader import download_audio_from_channel, download_audio
from transcriber import transcribe_audio
from file_manager import ensure_directories_exist, files_exist, sanitize_filename
import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up directories
PODCAST_AUDIO_DIR = './app/podcast_audio'
TRANSCRIPTIONS_DIR = './app/transcriptions'
ensure_directories_exist(PODCAST_AUDIO_DIR, TRANSCRIPTIONS_DIR)


# Function to download and transcribe a single video
def download_and_transcribe_video(video_info):
    """Download and transcribe a single video.

    This function checks if the audio file and transcription file already exist to avoid redundant processing.
    It also wraps download and transcription steps in try-except blocks to handle any errors gracefully.
    """
    title = video_info.get('title', 'Unknown Title')
    sanitized_title = sanitize_filename(title)

    # Check if audio and transcription files already exist
    audio_exists, transcription_exists = files_exist(sanitized_title)

    if audio_exists and transcription_exists:
        logging.info(f"Skipping '{title}' (already downloaded and transcribed)")
        return

    # Download audio if it doesn't exist
    if not audio_exists:
        try:
            logging.info(f"Downloading '{title}'...")
            video_url = f"https://www.youtube.com/watch?v={video_info['id']}"
            download_audio(video_url)
            time.sleep(10)  # Avoid bot detection
        except Exception as e:
            logging.error(f"Failed to download '{title}': {e}")
            return  # Exit early if download fails

    # Transcribe audio if it doesn't exist
    audio_file = os.path.join(PODCAST_AUDIO_DIR, f"{sanitized_title}.mp3")
    if not transcription_exists:
        try:
            logging.info(f"Transcribing '{title}'...")
            transcribe_audio(audio_file, sanitized_title, TRANSCRIPTIONS_DIR)
        except Exception as e:
            logging.error(f"Failed to transcribe '{title}': {e}")


# Function to download and transcribe videos in a channel in parallel
def download_and_transcribe(channel_url, max_workers=4):
    """Download and transcribe all videos from a YouTube channel URL.

    This function uses parallel processing to handle multiple downloads and transcriptions simultaneously,
    making it faster to process large channels or playlists. The `max_workers` parameter controls the number
    of tasks that can run in parallel, allowing users to adjust it based on their system’s capabilities.

    **Why Use Parallel Processing?**
    - By using parallel processing, we can significantly speed up the download and transcription process,
      especially when dealing with a large number of videos.
    - Instead of processing one video at a time, this function allows us to handle multiple tasks concurrently,
      making better use of available system resources.

    **Adjusting max_workers for Performance**
    - The `max_workers` parameter defines the maximum number of videos processed at the same time.
    - Increasing `max_workers` can improve speed but may lead to higher CPU and memory usage.
    - Decreasing `max_workers` reduces resource usage but slows down processing.
    - If you find your system is overloaded, try lowering `max_workers` to a number that balances performance with system capacity.

    Args:
        channel_url (str): URL of the YouTube channel to download and transcribe videos from.
        max_workers (int): Maximum number of concurrent tasks for parallel processing.
    """
    # Fetch video entries from the channel
    try:
        video_entries = download_audio_from_channel(channel_url)
    except Exception as e:
        logging.error(f"Failed to fetch videos from channel '{channel_url}': {e}")
        return

    # Use ThreadPoolExecutor to process videos in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_and_transcribe_video, video_info) for video_info in video_entries]

        # Track completed tasks and handle results
        for future in as_completed(futures):
            try:
                future.result()  # Retrieves the result or raises the exception
            except Exception as e:
                logging.error(f"An error occurred during download/transcription: {e}")


# Example usage
if __name__ == "__main__":
    channel_url = ''  # Add the YouTube channel URL here
    download_and_transcribe(channel_url)
