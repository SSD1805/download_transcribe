from src.download_pipeline.download_manager import DownloadManager
from src.download_pipeline.youtube_downloader import YouTubeDownloader
from src.core.performance_tracker import PerformanceTracker

def main():
    # Initialize necessary components
    download_manager = DownloadManager(download_directory='app/audio_files')
    performance_manager = PerformanceTracker()

    # Create the YouTubeDownloader instance
    youtube_downloader = YouTubeDownloader(download_manager, performance_manager)

    # Example operations
    youtube_downloader.download_video("https://youtube.com/watch?v=example_video_id")
    youtube_downloader.download_channel("https://youtube.com/channel/example_channel_id")
    youtube_downloader.download_playlist("https://youtube.com/playlist?list=example_playlist_id")
    youtube_downloader.download_batch([
        "https://youtube.com/watch?v=video1",
        "https://youtube.com/watch?v=video2",
        "https://youtube.com/watch?v=video3"
    ])

if __name__ == "__main__":
    main()
