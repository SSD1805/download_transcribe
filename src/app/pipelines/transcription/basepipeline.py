import os

from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class BasePipeline:
    """
    A base class for pipelines that provides shared functionality such as
    logging, performance tracking, and file handling.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.logger],
        tracker=Provide[AppContainer.performance_tracker],
    ):
        self.logger = logger
        self.performance_tracker = tracker

    def track(self, task_name):
        """
        Wrapper for performance tracking.
        Args:
            task_name (str): The name of the task to track.
        """
        return self.performance_tracker.track_execution(task_name)

    def ensure_directory_exists(self, directory: str):
        """
        Ensure a directory exists, creating it if necessary.
        Args:
            directory (str): The path to the directory.
        """
        if not os.path.exists(directory):
            self.logger.info(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)

    def get_files_with_extensions(self, directory: str, extensions: tuple):
        """
        Get a list of files with specific extensions in a directory.
        Args:
            directory (str): The directory to search.
            extensions (tuple): The allowed file extensions.
        Returns:
            list: A list of file paths.
        """
        if not os.path.exists(directory):
            self.logger.error(f"Directory '{directory}' does not exist.")
            return []

        files = [f for f in os.listdir(directory) if f.lower().endswith(extensions)]
        self.logger.info(
            f"Found {len(files)} files in '{directory}' with extensions {extensions}."
        )
        return files
