from typing import Any, Callable, Union
from threading import Lock
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer

class ConfigurationRegistry:
    _lock = Lock()  # Thread-safe lock for lazy-loaded configs

    @inject
    def __init__(self, logger=Provide[AppContainer.logger], base_registry=Provide[AppContainer.base_registry]):
        """
        Initialize the ConfigurationRegistry.

        Args:
            logger: Logger instance for logging purposes.
            base_registry: Base registry instance for extending registry functionality.
        """
        self.logger = logger
        self.base_registry = base_registry
        self._lazy_loaded_configs: dict[str, Union[Any, Callable[[], Any]]] = {}

    def register(self, name: str, config: Union[Any, Callable[[], Any]], lazy_load: bool = False):
        """
        Register a configuration value.

        Args:
            name (str): The name of the configuration.
            config (Any or Callable[[], Any]): The configuration value or a callable that returns it.
            lazy_load (bool): Whether to lazy-load the configuration.
        """
        if lazy_load:
            with self._lock:
                self._lazy_loaded_configs[name] = config
                self.logger.info(f"Lazy configuration '{name}' registered.")
        else:
            self.base_registry.register(name, config)
            self.logger.info(f"Configuration '{name}' registered immediately.")

    def get(self, name: str) -> Any:
        """
        Retrieve a configuration value by name. If the configuration is lazy-loaded, it will be initialized.

        Args:
            name (str): The name of the configuration.

        Returns:
            Any: The configuration value.
        """
        if name in self._lazy_loaded_configs:
            with self._lock:
                # Double-check to avoid race conditions
                if name in self._lazy_loaded_configs:
                    config = self._lazy_loaded_configs.pop(name)
                    if callable(config):
                        config = config()  # Call the lazy-loaded function to get the actual config
                    self.base_registry.register(name, config)
                    self.logger.info(f"Lazy configuration '{name}' loaded and registered.")
                    return config

        return self.base_registry.get(name)

# This instantiation is handled by the AppContainer, so we do not need to manually instantiate it:
# configuration_registry = ConfigurationRegistry()
