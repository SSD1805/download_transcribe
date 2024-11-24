import threading

from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class ConfigManager:
    """
    Singleton class for managing configuration with thread-safe access.
    """

    _lock = threading.Lock()
    _instance = None

    @inject
    def __new__(
        cls,
        config_data: dict = Provide[
            AppContainer.config_data
        ],  # Injected config dictionary
        logger=Provide[AppContainer.logger],
    ):
        """Ensure ConfigManager is a singleton."""
        if not hasattr(cls, "_instance") or cls._instance is None:
            with cls._lock:
                if not hasattr(cls, "_instance") or cls._instance is None:
                    cls._instance = super(ConfigManager, cls).__new__(cls)
                    cls._instance._init_instance(config_data, logger)
        return cls._instance

    def _init_instance(self, config_data, logger):
        """
        Initialize instance variables.
        """
        self.config_data = config_data
        self.logger = logger

    def get(self, key, default=None):
        """
        Retrieve a value from the configuration.

        Args:
            key (str): The key to retrieve.
            default: The default value to return if the key is not found.

        Returns:
            The value associated with the key or the default value.
        """
        value = self.config_data.get(key, default)
        if value is None:
            self.logger.warning(
                f"Configuration key '{key}' not found. Returning default: {default}"
            )
        return value

    def reload_config(self, new_config_data: dict):
        """
        Reload configuration with new data.

        Args:
            new_config_data (dict): The new configuration data to load.
        """
        with self._lock:  # Ensure thread safety
            self.config_data = new_config_data
            self.logger.info("Configuration reloaded.")
            self._notify_reloaded()

    def _notify_reloaded(self):
        """
        Notify observers of configuration reload.
        """
        self.logger.info(
            "Configuration has been reloaded and may affect dependent services."
        )
