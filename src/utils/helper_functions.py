import os
import re
import logging
from tqdm import tqdm
from logger import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

class HelperFunctions:
    def __init__(self, log_file_path='app/logs/app.log'):
        """
        Initialize the HelperFunctions class with an optional path to the log file.

        Args:
            log_file_path (str): The path to the log file for logging messages.
        """
        self.log_file_path = log_file_path
        self._configure_logging()

    def _configure_logging(self):
        """
        Configure the logging setup for the application.
        """
        logging.basicConfig(
            filename=self.log_file_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Logging initialized.")

    def sanitize_filename(self, filename):
        """
        Sanitize the given filename to remove any invalid characters.

        Args:
            filename (str): The filename to sanitize.

        Returns:
            str: The sanitized filename.
        """
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        logging.info(f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    def format_timestamp(self, seconds):
        """
        Format a time in seconds into a formatted timestamp (e.g., HH:MM:SS).

        Args:
            seconds (int or float): The number of seconds to format.

        Returns:
            str: The formatted timestamp.
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        sec = int(seconds % 60)
        formatted_time = f"{hours:02}:{minutes:02}:{sec:02}"
        logging.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time

    def progress_bar(self, iterable, description="Processing"):
        """
        Wrap an iterable with a progress bar using tqdm.

        Args:
            iterable (iterable): The iterable to wrap.
            description (str): A description for the progress bar.

        Returns:
            tqdm: The wrapped iterable with a progress bar.
        """
        return tqdm(iterable, desc=description)

    def log_message(self, message, log_level='INFO'):
        """
        Log a message to the configured log file.

        Args:
            message (str): The message to log.
            log_level (str): The level of the log (e.g., 'INFO', 'ERROR').
        """
        if log_level.upper() == 'INFO':
            logging.info(message)
        elif log_level.upper() == 'ERROR':
            logging.error(message)
        elif log_level.upper() == 'WARNING':
            logging.warning(message)
        elif log_level.upper() == 'DEBUG':
            logging.debug(message)
        else:
            logging.info(message)

# Example usage
if __name__ == "__main__":
    helper = HelperFunctions()
    filename = helper.sanitize_filename("Example:File/Name.txt")
    print(f"Sanitized filename: {filename}")
    formatted_time = helper.format_timestamp(4000)
    print(f"Formatted timestamp: {formatted_time}")
