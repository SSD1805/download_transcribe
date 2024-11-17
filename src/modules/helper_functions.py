from src.utils.file_utilities import FilenameSanitizer
from src.utils.timestamp_formatter import TimestampFormatter
from src.utils.progress_bar import ProgressBar
from src.utils.message_logger import MessageLogger
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


class HelperFunctions:
    def __init__(self):
        self.logger = logger

    @perf_tracker.track
    def sanitize_filename(self, file_name):
        """
        Sanitizes the given filename and logs the result.

        Args:
            file_name (str): The filename to sanitize.

        Returns:
            str: The sanitized filename.
        """
        sanitized_name = FilenameSanitizer.sanitize_filename(file_name)
        self.logger.info(f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    @perf_tracker.track
    def format_timestamp(self, total_seconds):
        """
        Formats the timestamp from seconds to a human-readable format.

        Args:
            total_seconds (int): The timestamp in seconds.

        Returns:
            str: The formatted timestamp.
        """
        formatted_time = TimestampFormatter.format_timestamp(total_seconds)
        self.logger.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time

    def progress_bar(self, iterable, description="Processing"):
        """
        Displays a progress bar for the given iterable.

        Args:
            iterable (iterable): The iterable to wrap with a progress bar.
            description (str): The description for the progress bar.

        Returns:
            iterable: The wrapped iterable with a progress bar.
        """
        return ProgressBar.progress_bar(iterable, description)

    def log_message(self, log_message, log_level='INFO'):
        """
        Logs a message with the specified log level.

        Args:
            log_message (str): The message to log.
            log_level (str): The log level (default is 'INFO').
        """
        MessageLogger.log_message(log_message, log_level)


# Example usage
if __name__ == "__main__":
    helper = HelperFunctions()
    sanitized_filename = helper.sanitize_filename("Example:File/Name.txt")
    print(f"Sanitized filename: {sanitized_filename}")
    formatted_time = helper.format_timestamp(4000)
    print(f"Formatted timestamp: {formatted_time}")
    for _ in helper.progress_bar(range(10), description="Processing"):
        pass
    helper.log_message("This is an info message.")

from src.utils.file_utilities import FilenameSanitizer
from src.utils.timestamp_formatter import TimestampFormatter
from src.utils.progress_bar import ProgressBar
from src.utils.message_logger import MessageLogger

class HelperFunctions:
    @staticmethod
    def sanitize_filename(file_name):
        return FilenameSanitizer.sanitize(file_name)

    @staticmethod
    def format_timestamp(total_seconds):
        return TimestampFormatter.format(total_seconds)

    @staticmethod
    def progress_bar(iterable, description="Processing"):
        return ProgressBar.wrap(iterable, description)

    @staticmethod
    def log_message(log_message, log_level='INFO'):
        MessageLogger.log(log_message, log_level)
