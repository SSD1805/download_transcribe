# message_logger_test.py
import logging

class MessageLogger:
    @staticmethod
    def log_message(message, log_level='INFO'):
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