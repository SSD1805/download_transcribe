# src/utils/file_utilities.py
import os
import shutil
from typing import Optional

import arrow  # Arrow is a library for handling dates and times in Python.
import yaml
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class FileUtilityFacade:
    """
    Facade to handle all file-related operations including file management,
    directory management, YAML handling, timestamp management, and filename sanitization.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.logger],
        tracker=Provide[AppContainer.performance_tracker],
    ):
        self.logger = logger
        self.tracker = tracker

    # File Operations
    def save_file(self, content: bytes, file_path: str):
        """Save binary content to a specified file path."""
        with self.tracker.track_execution("Save File"):
            try:
                with open(file_path, "wb") as file:
                    file.write(content)
                self.logger.info(f"File saved successfully: {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to save file {file_path}: {e}")
                raise

    def load_file(self, file_path: str) -> bytes:
        """Load and return binary content from a file."""
        with self.tracker.track_execution("Load File"):
            try:
                with open(file_path, "rb") as file:
                    content = file.read()
                self.logger.info(f"File loaded successfully: {file_path}")
                return content
            except Exception as e:
                self.logger.error(f"Failed to load file {file_path}: {e}")
                raise

    def delete_file(self, file_path: str):
        """Delete a specified file."""
        with self.tracker.track_execution("Delete File"):
            try:
                os.remove(file_path)
                self.logger.info(f"File deleted successfully: {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to delete file {file_path}: {e}")
                raise

    def copy_file(self, source: str, destination: str):
        """Copy a file from source to destination."""
        with self.tracker.track_execution("Copy File"):
            try:
                shutil.copy2(source, destination)
                self.logger.info(f"File copied from {source} to {destination}")
            except Exception as e:
                self.logger.error(
                    f"Failed to copy file from {source} to {destination}: {e}"
                )
                raise

    # Directory Operations
    def ensure_directory_exists(self, directory_path: str):
        """Ensure a directory exists, creating it if necessary."""
        try:
            os.makedirs(directory_path, exist_ok=True)
            self.logger.info(f"Directory ensured: {directory_path}")
        except Exception as e:
            self.logger.error(f"Failed to ensure directory {directory_path}: {e}")
            raise

    def list_files(
        self, directory_path: str, extensions: Optional[tuple] = None
    ) -> list:
        """
        List files in a directory with optional filtering by extensions.

        Args:
            directory_path (str): Path of the directory to list files.
            extensions (tuple, optional): Tuple of file extensions to filter.

        Returns:
            list: List of file paths in the directory.
        """
        try:
            files = [
                os.path.join(directory_path, f)
                for f in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, f))
                and (not extensions or f.endswith(extensions))
            ]
            self.logger.info(
                f"Listed {len(files)} files in directory: {directory_path}"
            )
            return files
        except Exception as e:
            self.logger.error(
                f"Failed to list files in directory {directory_path}: {e}"
            )
            raise

    # YAML Parsing Operations
    def read_yaml(self, filepath: str):
        """Reads YAML data from a file."""
        self.logger.info(f"Reading YAML file at {filepath}.")
        try:
            with open(filepath) as file:
                data = yaml.safe_load(file)
            self.logger.info(f"YAML data read successfully from {filepath}.")
            return data
        except Exception as e:
            self.logger.error(f"Failed to read YAML file {filepath}: {e}")
            raise

    def write_yaml(self, data: dict, filepath: str):
        """Writes YAML data to a file."""
        self.logger.info(f"Writing YAML data to file at {filepath}.")
        try:
            with open(filepath, "w") as file:
                yaml.safe_dump(data, file)
            self.logger.info(f"YAML data written successfully to {filepath}.")
        except Exception as e:
            self.logger.error(f"Failed to write YAML file {filepath}: {e}")
            raise

    # Timestamp Utilities using Arrow
    def format_timestamp(self, timestamp=None):
        """Formats the given timestamp to 'YYYY-MM-DD HH:MM:SS'. Uses the current time if no timestamp is provided."""
        if timestamp is None:
            timestamp = arrow.now()
        formatted = timestamp.format("YYYY-MM-DD HH:mm:ss")
        self.logger.info(f"Formatted timestamp: {formatted}")
        return formatted

    def get_current_timestamp(self):
        """Returns the current timestamp using Arrow."""
        current_timestamp = arrow.now()
        self.logger.info(f"Current timestamp: {current_timestamp}")
        return current_timestamp

    # Filename Sanitization
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize a filename to make it safe for file systems."""
        sanitized = "".join(
            c if c.isalnum() or c in " ._-()" else "_" for c in filename
        )
        self.logger.info(f"Sanitized filename: {sanitized}")
        return sanitized
