from typing import Any, Callable, Union
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer

class ConfigurationRegistry:
    _instance = None  # Singleton instance

    @inject
    def __new__(cls, base_registry=Provide[AppContainer.generic_registry], concurrency=Provide[AppContainer.concurrency_utilities]):
        if not cls._instance:
            with concurrency.get_lock():  # Using concurrency utility lock for singleton instantiation
                if not cls._instance:
                    cls._instance = super(ConfigurationRegistry, cls).__new__(cls)
                    cls._instance._init_singleton(base_registry, concurrency)
        return cls._instance

    @inject
    def _init_singleton(self, base_registry, concurrency, logger=Provide[AppContainer.struct_logger], tracker=Provide[AppContainer.performance_tracker]):
        """
        Initialize the singleton instance.
        """
        self.base_registry = base_registry
        self.logger = logger
        self.tracker = tracker
        self.concurrency = concurrency
        self._lazy_loaded_configs: Dict[str, Union[Any, Callable[[], Any]]] = {}
        self.logger.info("Initialized ConfigurationRegistry singleton.")

    def register(self, name: str, config: Union[Any, Callable[[], Any]], lazy_load: bool = False):
        """
        Register a configuration value.

        Args:
            name (str): The name of the configuration.
            config (Any or Callable[[], Any]): The configuration value or a callable that returns it.
            lazy_load (bool): Whether to lazy-load the configuration.
        """
        with self.concurrency.get_lock():  # Using concurrency utility lock for thread safety
            with self.tracker.track_execution("Register Configuration Item"):
                if lazy_load:
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
        with self.concurrency.get_lock():  # Using concurrency utility lock for thread safety
            with self.tracker.track_execution("Get Configuration Item"):
                if name in self._lazy_loaded_configs:
                    # Double-check to avoid race conditions
                    config = self._lazy_loaded_configs.pop(name)
                    if callable(config):
                        config = config()  # Call the lazy-loaded function to get the actual config
                    self.base_registry.register(name, config)
                    self.logger.info(f"Lazy configuration '{name}' loaded and registered.")
                    return config

                return self.base_registry.get(name)

# Example Usage
if __name__ == "__main__":
    from infrastructure.dependency_setup import container

    # Wire the AppContainer dependencies to this module
    container.wire(modules=[__name__])

    # Get the singleton instance of ConfigurationRegistry
    config_registry = ConfigurationRegistry()

    # Register a lazy configuration
    config_registry.register("lazy_config", lambda: {"key": "value"}, lazy_load=True)

    # Register an immediate configuration
    config_registry.register("immediate_config", {"key": "immediate_value"})

    # Retrieve the lazy configuration (will initialize it)
    lazy_config_value = config_registry.get("lazy_config")
    print(f"Lazy Config Value: {lazy_config_value}")

    # Retrieve the immediate configuration
    immediate_config_value = config_registry.get("immediate_config")
    print(f"Immediate Config Value: {immediate_config_value}")
