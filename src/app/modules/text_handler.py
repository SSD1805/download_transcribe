from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class TextHandler:
    """
    Handles text processing tasks such as tokenization, segmentation, and NER.
    """

    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        self.logger = logger
        self.processed_data = []

    def load(self, file_path: str):
        """
        Load a single text file for processing.
        """
        self.logger.info(f"Loading file: {file_path}")
        with open(file_path) as file:
            content = file.read()
        self.logger.info(f"Loaded content from {file_path}.")
        self.processed_data.append(content)

    def process_tasks(self, tasks: str):
        """
        Process tasks such as tokenization, segmentation, and NER.

        Args:
            tasks (str): Comma-separated list of tasks to execute, or "all".
        """
        self.logger.info(f"Processing tasks: {tasks}")
        # Example task logic
        if tasks == "all":
            tasks = ["tokenization", "segmentation", "ner"]

        for task in tasks.split(","):
            self.logger.info(f"Executing task: {task.strip()}")
            # Mock task execution
            for i, data in enumerate(self.processed_data):
                self.processed_data[i] = f"{data} [{task.strip()}]"

    def get_processed_data(self):
        """
        Retrieve the processed data.

        Returns:
            list: The processed data.
        """
        self.logger.info("Retrieving processed data.")
        return self.processed_data
