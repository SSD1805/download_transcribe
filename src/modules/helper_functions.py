from src.core.logger_manager import LoggerManager
from src.utils.filename_sanitizer import FilenameSanitizer
from src.utils.timestamp_formatter import TimestampFormatter
from src.utils.progress_bar import ProgressBar
from src.utils.message_logger import MessageLogger

class HelperFunctions:
    def __init__(self):
        self.log_manager = LoggingManager()
        self.logger = self.log_manager.get_logger()

    def sanitize_filename(self, filename):
        sanitized_name = FilenameSanitizer.sanitize_filename(filename)
        self.logger.info(f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    def format_timestamp(self, seconds):
        formatted_time = TimestampFormatter.format_timestamp(seconds)
        self.logger.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time

    def progress_bar(self, iterable, description="Processing"):
        return ProgressBar.progress_bar(iterable, description)

    def log_message(self, message, log_level='INFO'):
        MessageLogger.log_message(message, log_level)

# Example usage
if __name__ == "__main__":
    helper = HelperFunctions()
    filename = helper.sanitize_filename("Example:File/Name.txt")
    print(f"Sanitized filename: {filename}")
    formatted_time = helper.format_timestamp(4000)
    print(f"Formatted timestamp: {formatted_time}")
    for _ in helper.progress_bar(range(10), description="Processing"):
        pass
    helper.log_message("This is an info message.")