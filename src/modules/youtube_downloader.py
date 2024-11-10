import os
import yt_dlp
from logger import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()


class YouTubeDownloader:
    def __init__(self, download_directory='app/audio_files', yt_dlp_options=None):
        # Attributes: store the download directory and options for yt-dlp
        self.download_directory = download_directory
        self.yt_dlp_options = yt_dlp_options or {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_directory, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

    def sanitize_filename(self, filename):
        # A simple method to sanitize filenames
        return "".join([c if c.isalnum() or c in " ._-()" else "_" for c in filename])

    def download_video(self, url):
        # Method to download a single YouTube video
        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as ydl:
                print(f"Downloading video from URL: {url}")
                ydl.download([url])
                print("Download completed.")
        except Exception as e:
            print(f"Error downloading video: {e}")

    def download_channel(self, channel_url):
        # Method to download all videos from a channel
        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as ydl:
                print(f"Downloading channel from URL: {channel_url}")
                ydl.download([channel_url])
                print("Channel download completed.")
        except Exception as e:
            print(f"Error downloading channel: {e}")

    def download_playlist(self, playlist_url):
        # Method to download all videos from a playlist
        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as ydl:
                print(f"Downloading playlist from URL: {playlist_url}")
                ydl.download([playlist_url])
                print("Playlist download completed.")
        except Exception as e:
            print(f"Error downloading playlist: {e}")