from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

class HelperFunctions:
    def sanitize_filename(self, file_name):
        sanitized_name = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in file_name)
        logger.info(f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    def format_timestamp(self, total_seconds):
        formatted_time = f"{total_seconds // 60}:{total_seconds % 60}"
        logger.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time
