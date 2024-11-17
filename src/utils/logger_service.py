import logging
import sys
from typing import Optional

# Singleton Pattern with Dependency Injection and Factory Method
class LoggerService:
    """
    Singleton LoggerService that provides a logger instance.
    Implements a factory pattern to create and configure a logger if none exists.
    """
    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_instance(cls, name='app_logger', level=logging.INFO, format_string=None) -> logging.Logger:
        """
        Returns the singleton instance of the logger.
        If no instance exists, it creates and configures one.

        Args:
            name (str): Name of the logger.
            level (int): Logging level (default: logging.INFO).
            format_string (str): Format string for log messages.

        Returns:
            logging.Logger: Configured logger instance.
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(name, level, format_string)
        return cls._instance

    @staticmethod
    def _create_logger(name, level, format_string) -> logging.Logger:
        """
        Factory method to create a new logger instance with a specified name, level, and format.

        Args:
            name (str): Name of the logger.
            level (int): Logging level.
            format_string (str): Format string for log messages.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Clear existing handlers to avoid duplicate logs in case of reinitialization
        if logger.hasHandlers():
            logger.handlers.clear()

        # Formatter
        if not format_string:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(format_string)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler (Optional: Can be used for persistent logging)
        file_handler = logging.FileHandler(f"{name}.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.debug("Logger initialized.")
        return logger

    @classmethod
    def set_log_level(cls, level: int) -> None:
        """
        Set the logging level for the logger instance.

        Args:
            level (int): Logging level to set.
        """
        if cls._instance:
            cls._instance.setLevel(level)
            cls._instance.info(f"Log level set to {logging.getLevelName(level)}")

    @classmethod
    def add_custom_handler(cls, handler: logging.Handler) -> None:
        """
        Add a custom handler to the logger instance.

        Args:
            handler (logging.Handler): Custom logging handler to be added.
        """
        if cls._instance:
            cls._instance.addHandler(handler)
            cls._instance.info(f"Custom handler {handler} added.")

# Example usage
if __name__ == "__main__":
    # Retrieve logger instance
    logger = LoggerService.get_instance(name="example_logger", level=logging.DEBUG)

    # Add custom handler (for example, an SMTPHandler for email notifications)
    smtp_handler = logging.handlers.SMTPHandler(
        mailhost=("smtp.example.com", 587),
        fromaddr="noreply@example.com",
        toaddrs=["admin@example.com"],
        subject="Application Error Alert",
        credentials=("user", "password"),
        secure=()
    )
    LoggerService.add_custom_handler(smtp_handler)

    # Log messages
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.error("This is an error message.")
