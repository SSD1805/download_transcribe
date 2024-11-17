from src.pipelines.download.download_manager import DownloadManager
from src.pipelines.download import YouTubeDownloader
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()

def main():
    try:
        # Initialize necessary components
        download_manager = DownloadManager()
        performance_tracker = PerformanceTracker()
        youtube_downloader = YouTubeDownloader(download_manager, performance_tracker)

        # Log start of operations
        logger.info("Starting YouTube download operations.")

        # Example operations with logging
        logger.info("Downloading single video...")
        youtube_downloader.download_video("https://youtube.com/watch?v=example_video_id")
        logger.info("Single video download completed.")

        logger.info("Downloading channel videos...")
        youtube_downloader.download_channel("https://youtube.com/channel/example_channel_id")
        logger.info("Channel download completed.")

        logger.info("Downloading playlist videos...")
        youtube_downloader.download_playlist("https://youtube.com/playlist?list=example_playlist_id")
        logger.info("Playlist download completed.")

        logger.info("Downloading a batch of videos...")
        youtube_downloader.download_batch([
            "https://youtube.com/watch?v=video1",
            "https://youtube.com/watch?v=video2",
            "https://youtube.com/watch?v=video3"
        ])
        logger.info("Batch video download completed.")

    except Exception as e:
        logger.error(f"An error occurred during YouTube download operations: {e}")

if __name__ == "__main__":
    main()
