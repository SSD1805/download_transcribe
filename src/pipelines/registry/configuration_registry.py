# src/registry/configuration_registry.py
from typing import Any
from src.registry.base_registry import BaseRegistry
import logging

class ConfigurationRegistry(BaseRegistry[Any]):
    """
    A registry for managing configuration settings for different services and components.
    Includes specialized behavior for handling lazy loading and logging of configuration changes.
    """
    def __init__(self):
        super().__init__()
        self._lazy_loaded_configs = {}
        self.logger = logging.getLogger("ConfigurationRegistry")

    def register(self, name: str, config: Any, lazy_load: bool = False):
        """
        Register a configuration setting.

        Args:
            name (str): The name of the configuration.
            config (Any): The configuration object or a callable to retrieve it.
            lazy_load (bool): If True, the configuration will be loaded only when accessed.
        """
        if lazy_load:
            self._lazy_loaded_configs[name] = config
            self.logger.info(f"Lazy configuration '{name}' registered.")
        else:
            super().register(name, config)
            self.logger.info(f"Configuration '{name}' registered immediately.")

    def get(self, name: str) -> Any:
        """
        Retrieve a configuration setting by name.

        Args:
            name (str): The name of the configuration.

        Returns:
            Any: The configuration setting.
        """
        if name in self._lazy_loaded_configs:
            config = self._lazy_loaded_configs.pop(name)
            if callable(config):
                config = config()
            super().register(name, config)
            self.logger.info(f"Lazy configuration '{name}' loaded and registered.")
            return config
        return super().get(name)

# Initialize the ConfigurationRegistry
configuration_registry = ConfigurationRegistry()

# Register configuration settings
configuration_registry.register("database_settings", DatabaseSettings, lazy_load=True)
configuration_registry.register("api_keys", APIKeyManager)
configuration_registry.register("ml_model_config", ModelConfiguration, lazy_load=True)
