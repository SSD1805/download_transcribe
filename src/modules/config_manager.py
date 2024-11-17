# config_manager.py
import yaml
import os
from src.core.services import CoreServices

# Initialize logger and performance tracker
logger = CoreServices.get_logger()
perf_tracker = LoggerService.get_instance()

class ConfigManager:
    def __init__(self, config_path='config.yaml', logger=None):
        """
        Initialize the ConfigManager with configuration and performance tracking.

        Args:
            config_path (str): Path to the YAML configuration file.
            logger (Logger, optional): Logger instance for logging messages. Defaults to a logger created by LoggerManager.
        """
        self.config_path = config_path
        self.logger = logger or LoggerManager().get_logger()
        self.config_data = self._load_config()
        self.performance_tracker = PerformanceTracker()  # Initialize performance tracking

        # Optionally configure performance tracking settings from config
        self._configure_performance_tracker()

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

    def _configure_performance_tracker(self):
        """
        Configure performance tracking based on settings in the config file.
        """
        performance_settings = self.config_data.get("performance", {})
        monitor_interval = performance_settings.get("monitor_interval", 5)
        self.performance_tracker.monitor_memory_usage(interval=monitor_interval)
        self.logger.info(f"Performance tracker configured with interval: {monitor_interval} seconds")

    def get_performance_tracker(self):
        """
        Returns the initialized PerformanceTracker instance.

        Returns:
            PerformanceTracker: Instance of PerformanceTracker.
        """
        return self.performance_tracker

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

from yaml_parser import YAMLParser

class ConfigManager:
    def __init__(self, config_path, performance_configurator=None):
        self.config_path = config_path
        self.config_data = YAMLParser.parse(config_path)
        self.performance_configurator = performance_configurator

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def validate_keys(self, required_keys):
        missing_keys = [key for key in required_keys if key not in self.config_data]
        if missing_keys:
            raise KeyError(f"Missing required configuration keys: {', '.join(missing_keys)}")

    def configure_performance(self):
        if self.performance_configurator:
            self.performance_configurator.configure(self.config_data.get("performance", {}))

# Example usage
if __name__ == "__main__":
    config_manager = ConfigManager(config_path='config.yaml')
    performance_tracker = config_manager.get_performance_tracker()
    # Now, you can use performance_tracker to track performance in other modules
