import os
import shutil
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker
from typing import Optional

# Logger and Tracker Instances
logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

class FileManager:
    """
    Handles file operations such as saving, loading, copying, and deleting files.
    """
    def __init__(self, logger=logger, tracker=perf_tracker):
        self.logger = logger
        self.tracker = tracker

    @perf_tracker.track
    def save_file(self, content: bytes, file_path: str):
        """
        Save binary content to a specified file path.

        Args:
            content (bytes): Content to save.
            file_path (str): Destination file path.
        """
        try:
            with open(file_path, 'wb') as file:
                file.write(content)
            self.logger.info(f"File saved successfully: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to save file {file_path}: {e}")
            raise

    @perf_tracker.track
    def load_file(self, file_path: str) -> bytes:
        """
        Load and return binary content from a file.

        Args:
            file_path (str): Path of the file to load.

        Returns:
            bytes: File content.
        """
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            self.logger.info(f"File loaded successfully: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Failed to load file {file_path}: {e}")
            raise

    @perf_tracker.track
    def delete_file(self, file_path: str):
        """
        Delete a specified file.

        Args:
            file_path (str): Path of the file to delete.
        """
        try:
            os.remove(file_path)
            self.logger.info(f"File deleted successfully: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {e}")
            raise

    @perf_tracker.track
    def copy_file(self, source: str, destination: str):
        """
        Copy a file from source to destination.

        Args:
            source (str): Path of the source file.
            destination (str): Destination path for the copied file.
        """
        try:
            shutil.copy2(source, destination)
            self.logger.info(f"File copied from {source} to {destination}")
        except Exception as e:
            self.logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            raise

class DirectoryManager:
    """
    Handles directory operations such as ensuring existence, listing files, and creating directories.
    """
    def __init__(self, logger=logger):
        self.logger = logger

    def ensure_directory_exists(self, directory_path: str):
        """
        Ensure a directory exists, creating it if necessary.

        Args:
            directory_path (str): Path of the directory to check or create.
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            self.logger.info(f"Directory ensured: {directory_path}")
        except Exception as e:
            self.logger.error(f"Failed to ensure directory {directory_path}: {e}")
            raise

    def list_files(self, directory_path: str, extensions: Optional[tuple] = None) -> list:
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
            self.logger.info(f"Listed {len(files)} files in directory: {directory_path}")
            return files
        except Exception as e:
            self.logger.error(f"Failed to list files in directory {directory_path}: {e}")
            raise

class FilenameSanitizer:
    """
    Provides utilities for sanitizing file names.
    """
    def __init__(self, logger=logger):
        self.logger = logger

    def sanitize(self, filename: str) -> str:
        """
        Sanitize a filename to make it safe for file systems.

        Args:
            filename (str): Filename to sanitize.

        Returns:
            str: Sanitized filename.
        """
        sanitized = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in filename)
        self.logger.info(f"Sanitized filename: {sanitized}")
        return sanitized
