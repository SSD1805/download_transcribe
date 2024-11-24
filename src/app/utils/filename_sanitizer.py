from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class FilenameSanitizer:
    """
    Handles filename sanitization to ensure compatibility with file systems.
    """

    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        self.logger = logger

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename to make it safe for file systems.

        Args:
            filename (str): The original filename.

        Returns:
            str: The sanitized filename.
        """
        sanitized = "".join(
            c if c.isalnum() or c in " ._-()" else "_" for c in filename
        )
        self.logger.info(f"Sanitized filename: {sanitized}")
        return sanitized
