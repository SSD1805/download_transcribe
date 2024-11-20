from dependency_injector.wiring import inject, Provide
from infrastructure.dependency_setup import AppContainer


class HelperFunctions:
    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        self.logger = logger

    @staticmethod
    def sanitize_filename(file_name: str) -> str:
        """
        Sanitize the given file name by removing any invalid characters.

        Args:
            file_name (str): The file name to sanitize.

        Returns:
            str: The sanitized file name.
        """
        sanitized_name = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in file_name)
        return sanitized_name

    @staticmethod
    def format_timestamp(total_seconds: int) -> str:
        """
        Format the given total number of seconds as a timestamp in mm:ss format.

        Args:
            total_seconds (int): Total number of seconds to format.

        Returns:
            str: The formatted timestamp as a string.
        """
        minutes, seconds = divmod(total_seconds, 60)
        formatted_time = f"{minutes:02}:{seconds:02}"
        return formatted_time

    def log_sanitized_filename(self, file_name: str) -> str:
        """
        Sanitize the given file name and log the action.

        Args:
            file_name (str): The file name to sanitize.

        Returns:
            str: The sanitized file name.
        """
        sanitized_name = self.sanitize_filename(file_name)
        self.logger.info(f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    def log_formatted_timestamp(self, total_seconds: int) -> str:
        """
        Format the given total number of seconds and log the action.

        Args:
            total_seconds (int): Total number of seconds to format.

        Returns:
            str: The formatted timestamp as a string.
        """
        formatted_time = self.format_timestamp(total_seconds)
        self.logger.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time
