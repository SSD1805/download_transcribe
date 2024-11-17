# src/core/exception_handler.py
def handle_exception(exception, logger, message):
    logger.error(f"{message}: {exception}")
    raise exception
