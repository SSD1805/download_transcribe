from src.celery_tasks.download_tasks import download_video_task
from src.pipelines.download.download_handler import DownloadManager
from src.modules.config_manager import ConfigManager
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

def main():
    # Initialize configuration
    config_manager = ConfigManager(config_path='config.yaml')

    # Asynchronous task
    download_video_task.delay("https://youtube.com/watch?v=example_video_id", config_manager)

    # Synchronous download
    download_manager = DownloadManager(config_manager)
    download_manager.download("https://youtube.com/watch?v=another_video_id")

if __name__ == "__main__":
    main()
