from src.utils.structlog_logger import StructLogger
import pendulum

logger = StructLogger.get_logger()

class TimestampFormatter:
    @staticmethod
    def format(seconds: int) -> str:
        """
        Formats seconds into a human-readable HH:MM:SS format using pendulum.

        Args:
            seconds (int): Total time in seconds.

        Returns:
            str: Formatted time as HH:MM:SS.
        """
        duration = pendulum.duration(seconds=seconds)
        formatted_time = duration.format("HH:mm:ss", formatter="alternative")
        logger.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time