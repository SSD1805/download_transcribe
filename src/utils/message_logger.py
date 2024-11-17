import logging

class MessageLogger:
    @staticmethod
    def log(message: str, log_level: str = 'INFO'):
        """
        Logs a message with the specified log level.

        Args:
            message (str): The message to log.
            log_level (str): The log level (e.g., 'INFO', 'ERROR').
        """
        log_levels = {
            'INFO': logging.info,
            'ERROR': logging.error,
            'WARNING': logging.warning,
            'DEBUG': logging.debug,
        }
        log_function = log_levels.get(log_level.upper(), logging.info)
        log_function(message)
