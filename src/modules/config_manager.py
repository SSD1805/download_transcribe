import os
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker
from src.utils.yaml_parser import YAMLParser

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

class ConfigManager:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")

        try:
            with open(self.config_path, 'r') as config_file:
                config_data = YAMLParser.safe_load(config_file)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config_data
        except Exception as e:
            logger.error(f"Error parsing YAML file {self.config_path}: {e}")
            raise

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def reload_config(self):
        self.config_data = self._load_config()
        logger.info("Configuration reloaded.")
