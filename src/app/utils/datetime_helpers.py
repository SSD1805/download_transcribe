import pendulum
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class TimestampUtilities:
    """
    A utility class for timestamp-related operations using Pendulum.
    """

    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        self.logger = logger

    def format_timestamp(self, timestamp=None):
        """
        Formats the given timestamp to 'YYYY-MM-DD HH:MM:SS'.
        Uses the current time if no timestamp is provided.

        Args:
            timestamp (pendulum.DateTime, optional): The timestamp to format. Defaults to None.

        Returns:
            str: The formatted timestamp as a string.
        """
        if timestamp is None:
            timestamp = pendulum.now()
        formatted = timestamp.format("YYYY-MM-DD HH:mm:ss")
        self.logger.info(f"Formatted timestamp: {formatted}")
        return formatted

    def get_current_timestamp(self):
        """
        Returns the current timestamp using Pendulum.

        Returns:
            pendulum.DateTime: The current timestamp.
        """
        current_timestamp = pendulum.now()
        self.logger.info(f"Current timestamp: {current_timestamp}")
        return current_timestamp

    def log_formatted_timestamp(self, total_seconds: int) -> str:
        """
        Format the given total number of seconds as a timestamp and log the action.

        Args:
            total_seconds (int): Total number of seconds to format.

        Returns:
            str: The formatted timestamp as a string.
        """
        formatted_time = self.format_timestamp(pendulum.duration(seconds=total_seconds))
        self.logger.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time
