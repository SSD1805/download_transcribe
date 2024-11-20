from dependency_injector.wiring import inject, Provide
from src.infrastructure.dependency_setup import AppContainer
import threading
import os

class ConfigManager:
    """Singleton class for managing configuration using a centralized approach."""

    # Thread lock for thread safety
    _lock = threading.Lock()

    @inject
    def __init__(self, config_path: str = Provide[AppContainer.config_path],
                 logger=Provide[AppContainer.logger],
                 yaml_parser=Provide[AppContainer.yaml_parser]):
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
            except Exception as e:
                self.logger.error(f"Error parsing YAML file {self.config_path}: {e}")
                raise

    def get(self, key, default=None):
        """Retrieve a value from the configuration."""
        return self.config_data.get(key, default)

    def reload_config(self):
        """Reload configuration from the config file."""
        with self._lock:  # Ensure thread safety
            self.config_data = self._load_config()
            self.logger.info("Configuration reloaded.")
            # Notify other parts of the application if required
            self._notify_reloaded()

    def _notify_reloaded(self):
        """Optional: Notify other components of config reload (to be implemented)."""
        # Here you could add logic to inform other parts of the system that
        # the configuration has been reloaded. This can be implemented using
        # observer patterns or simply re-injecting configuration in components.
        self.logger.info("Notification: Configuration has been reloaded and may affect dependent services.")
