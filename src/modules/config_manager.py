import yaml
import os
from src.core.logger_manager import LoggerManager


class ConfigManager:
    def __init__(self, config_path='config.yaml', logger=None):
        """
        Initialize the ConfigManager with a specified path to the configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.
            logger (Logger, optional): Logger instance for logging messages. If not provided, a default will be created.
        """
        self.config_path = config_path
        self.logger = logger or LoggerManager().get_logger()
        self.config_data = self._load_config()

    def _load_config(self):
        """
        Load and parse the YAML configuration file.

        Returns:
            dict: Loaded configuration data.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            yaml.YAMLError: If there is an error in parsing the YAML file.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")

        try:
            with open(self.config_path, 'r') as config_file:
                config_data = yaml.safe_load(config_file)
                self.logger.info(f"Configuration loaded from {self.config_path}")
                return config_data
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML file {self.config_path}: {e}")
            raise

    def get(self, key, default=None):
        """
        Retrieve a value from the configuration using a key.

        Args:
            key (str): The key to look up in the configuration data.
            default: The default value to return if the key is not found.

        Returns:
            The value associated with the key or the default value.
        """
        value = self.config_data.get(key, default)
        if value is None:
            self.logger.warning(f"Configuration key '{key}' not found. Using default: {default}")
        return value

    def validate_keys(self, required_keys):
        """
        Validate the configuration to ensure required keys are present.

        Args:
            required_keys (list): List of keys that must be present in the configuration.

        Raises:
            KeyError: If any required key is missing from the configuration.
        """
        missing_keys = [key for key in required_keys if key not in self.config_data]
        if missing_keys:
            error_message = f"Missing required configuration keys: {', '.join(missing_keys)}"
            self.logger.error(error_message)
            raise KeyError(error_message)
        self.logger.info("All required configuration keys are present.")

    def reload_config(self):
        """
        Reload the configuration file to reflect any changes.
        """
        self.config_data = self._load_config()
        self.logger.info("Configuration reloaded.")


# Example usage
if __name__ == "__main__":
    config_manager = ConfigManager(config_path='config.yaml')
    required_keys = ['download', 'whisper', 'directories']
    config_manager.validate_keys(required_keys)
    download_delay = config_manager.get('download', {}).get('delay', 10)
    config_manager.logger.info(f"Download delay is set to: {download_delay} seconds")
