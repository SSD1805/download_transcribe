from typing import Any
from src.pipelines.registry.base_registry import BaseRegistry
from src.utils.structlog_logger import StructLogger

logger = StructLogger.get_logger()

class ConfigurationRegistry(BaseRegistry[Any]):
    def __init__(self):
        super().__init__()
        self._lazy_loaded_configs = {}

    def register(self, name: str, config: Any, lazy_load: bool = False):
        if lazy_load:
            self._lazy_loaded_configs[name] = config
            logger.info(f"Lazy configuration '{name}' registered.")
        else:
            super().register(name, config)
            logger.info(f"Configuration '{name}' registered immediately.")

    def get(self, name: str) -> Any:
        if name in self._lazy_loaded_configs:
            config = self._lazy_loaded_configs.pop(name)
            if callable(config):
                config = config()
            super().register(name, config)
            logger.info(f"Lazy configuration '{name}' loaded and registered.")
            return config
        return super().get(name)

# Initialize the ConfigurationRegistry
configuration_registry = ConfigurationRegistry()
