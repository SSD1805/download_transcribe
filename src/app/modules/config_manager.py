from dependency_injector.wiring import inject, Provide
from infrastructure.dependency_setup import AppContainer
import threading
import os

class ConfigManager:
    """Singleton class for managing configuration using a centralized approach."""

    # Thread lock for thread safety
    _lock = threading.Lock()
    _instance = None

    @inject
    def __new__(cls,
                config_path: str = Provide[AppContainer.config_path],
                logger=Provide[AppContainer.logger],
                yaml_parser=Provide[AppContainer.yaml_parser]):
        """Ensure ConfigManager is a singleton."""
        if not hasattr(cls, '_instance') or cls._instance is None:
            with cls._lock:
                if not hasattr(cls, '_instance') or cls._instance is None:
                    cls._instance = super(ConfigManager, cls).__new__(cls)
                    cls._instance._init_instance(config_path, logger, yaml_parser)
        return cls._instance

    def _init_instance(self, config_path, logger, yaml_parser):
        """Initialization method to set instance variables."""
        self.config_path = config_path or os.getenv('CONFIG_PATH', '/app/config/config.yaml')
        self.logger = logger
        self.yaml_parser = yaml_parser
        self.config_data = self._load_config()

    def _load_config(self):
        """Load configuration from YAML file."""
        with self._lock:  # Ensure thread safety
            if not os.path.exists(self.config_path):
                self.logger.error(f"Configuration file not found at {self.config_path}")
                raise FileNotFoundError(f"Configuration file not found at {self.config_path}")

            try:
                with open(self.config_path, 'r') as config_file:
                    config_data = self.yaml_parser.safe_load(config_file)
                    self.logger.info(f"Configuration loaded from {self.config_path}")
                    return config_data
            except FileNotFoundError as e:
                self.logger.error(f"Configuration file not found: {e}")
                raise
            except Exception as e:
                self.logger.error(f"Error parsing YAML file {self.config_path}: {e}")
                raise

    def get(self, key, default=None):
        """Retrieve a value from the configuration."""
        value = self.config_data.get(key, default)
        if value is None:
            self.logger.warning(f"Configuration key '{key}' not found. Returning default: {default}")
        return value

    def reload_config(self):
        """Reload configuration from the config file."""
        with self._lock:  # Ensure thread safety
            self.config_data = self._load_config()
            self.logger.info("Configuration reloaded.")
            self._notify_reloaded()

    def _notify_reloaded(self):
        """Optional: Notify other components of config reload (to be implemented)."""
        # Add observer pattern here if needed to notify other parts of the system
        self.logger.info("Notification: Configuration has been reloaded and may affect dependent services.")

