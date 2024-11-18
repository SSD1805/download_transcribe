# download_coordinator.py

from src.celery_tasks.download_tasks import download_video_task
from src.pipelines.download.download_handler import DownloadManager
from src.modules.config_manager import ConfigManager
from src.utils.logger_service import LoggerService
from src.utils.performance_tracker import PerformanceTrackerService
# Get logger and performance tracker from CoreServices
logger = LoggerService.get_logger()
perf_tracker = PerformanceTrackerService.get_performance_tracker()

def main():
    # Initialize configuration and performance tracker
    config_manager = ConfigManager(config_path='config.yaml')
    perf_tracker = PerformanceTracker()

    # For asynchronous task
    download_video_task.delay("https://youtube.com/watch?v=example_video_id", config_manager)

    # For synchronous download (only use directly if immediate blocking behavior is needed)
    download_manager = DownloadManager(config_manager)
    download_manager.download("https://youtube.com/watch?v=another_video_id")

if __name__ == "__main__":
    main()
