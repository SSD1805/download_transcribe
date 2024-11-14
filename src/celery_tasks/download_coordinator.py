# download_coordinator.py

from src.celery_tasks.download_tasks import download_video_task
from src.download_pipeline.download_manager import DownloadManager
from src.core.performance_tracker import PerformanceTracker
from src.modules.config_manager import ConfigManager

def main():
    # Initialize configuration and performance tracker
    config_manager = ConfigManager(config_path='config.yaml')
    performance_manager = PerformanceTracker()

    # For asynchronous task
    download_video_task.delay("https://youtube.com/watch?v=example_video_id", config_manager)

    # For synchronous download (only use directly if immediate blocking behavior is needed)
    download_manager = DownloadManager(config_manager)
    download_manager.download("https://youtube.com/watch?v=another_video_id")

if __name__ == "__main__":
    main()