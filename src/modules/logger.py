import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os
from tenacity import retry, stop_after_attempt, wait_fixed

# Load environment variables from .env file
load_dotenv()


class LoggerManager:
    def __init__(self):
        self.log_file_path = os.getenv('LOG_FILE_PATH', '/app/logs/my_app.log')
        self.log_level = int(os.getenv('LOG_LEVEL', logging.INFO))
        self.log_max_bytes = int(os.getenv('LOG_MAX_BYTES', 10485760))  # Default: 10MB
        self.log_backup_count = int(os.getenv('LOG_BACKUP_COUNT', 5))
        self.enable_console_logging = os.getenv('ENABLE_CONSOLE_LOGGING', 'true').lower() == 'true'
        self.enable_file_logging = os.getenv('ENABLE_FILE_LOGGING', 'true').lower() == 'true'

        self.logger = logging.getLogger('app_logger')
        self.logger.setLevel(self.log_level)

        if not self.logger.handlers:
            self._configure_logger()

    def _configure_logger(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.enable_file_logging:
            file_handler = RotatingFileHandler(
                self.log_file_path, maxBytes=self.log_max_bytes, backupCount=self.log_backup_count
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if self.enable_console_logging:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


# Example usage with tenacity retry logic and finally block
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def critical_function_with_retry():
    logger = LoggerManager().get_logger()
    try:
        # Simulate a critical operation that might fail
        logger.info("Attempting a critical operation.")
        # Replace with actual logic (e.g., network call, file processing)
        raise ValueError("Simulated failure for retry.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise  # Ensure the exception is propagated for tenacity to handle
    finally:
        logger.info("Cleanup actions executed in finally block.")


if __name__ == "__main__":
    logger_manager = LoggerManager()
    logger = logger_manager.get_logger()
    logger.info("Logger initialized.")

    # Run the critical function with retry
    try:
        critical_function_with_retry()
    except Exception as e:
        logger.error(f"Final failure after retries: {e}")
