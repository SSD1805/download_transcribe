import pyyaml
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class YAMLManager:
    """
    Handles YAML reading and writing operations.
    """

    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        self.logger = logger

    def read_yaml(self, filepath: str) -> dict:
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
        self.logger.info(f"Writing YAML data to file at {filepath}.")
        try:
            with open(filepath, "w") as file:
                yaml.safe_dump(data, file)
            self.logger.info(f"YAML data written successfully to {filepath}.")
        except Exception as e:
            self.logger.error(f"Failed to write YAML file {filepath}: {e}")
            raise
