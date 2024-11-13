import yaml
import os
from logger_manager import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

class ConfigManager:
    def __init__(self, config_path='config.yaml'):
        """
        Initialize the ConfigManager with a specified path to the configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        self.config_path = config_path
        self.config_data = {}
        self.load_config()

    def load_config(self):
        """
        Load and parse the YAML configuration file.
        Raises:
            FileNotFoundError: If the configuration file is not found.
            yaml.YAMLError: If there is an error in parsing the YAML file.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r') as config_file:
                self.config_data = yaml.safe_load(config_file)
                logger.info(f"Configuration loaded from {self.config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise

    def get_value(self, key, default=None):
        """
        Retrieve a value from the configuration using a key.

        Args:
            key (str): The key to look up in the configuration data.
            default: The default value to return if the key is not found.

        Returns:
            The value associated with the key or the default value.
        """
        return self.config_data.get(key, default)

    def validate_config(self, required_keys):
        """
        Validate the configuration to ensure required keys are present.

        Args:
            required_keys (list): List of keys that must be present in the configuration.

        Raises:
            KeyError: If any required key is missing from the configuration.
        """
        missing_keys = [key for key in required_keys if key not in self.config_data]
        if missing_keys:
            logger.error(f"Missing required configuration keys: {', '.join(missing_keys)}")
            raise KeyError(f"Missing required configuration keys: {', '.join(missing_keys)}")
        logger.info("Configuration validated successfully.")

    def reload_config(self):
        """
        Reload the configuration file to reflect any changes.
        """
        self.load_config()
        logger.info("Configuration reloaded.")


# Example usage
if __name__ == "__main__":
    config_manager = ConfigManager(config_path='config.yaml')
    config_manager.validate_config(['download', 'whisper', 'directories'])
    download_delay = config_manager.get_value('download').get('delay', 10)
    logger.info(f"Download delay is set to: {download_delay} seconds")