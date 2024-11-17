class SettingsRegistry:
    """
    Registry to store and retrieve settings modules or configurations.
    """
    _settings = {}

    @staticmethod
    def register_settings(name, settings_instance):
        """
        Register a settings instance with a unique name.

        Args:
            name (str): The name for the settings (e.g., 'database', 'performance').
            settings_instance (object): The settings instance or module.
        """
        SettingsRegistry._settings[name] = settings_instance

    @staticmethod
    def get_settings(name):
        """
        Retrieve the settings instance by name.

        Args:
            name (str): The name of the settings to retrieve.

        Returns:
            object: The registered settings instance.

        Raises:
            ValueError: If the requested settings are not registered.
        """
        if name not in SettingsRegistry._settings:
            raise ValueError(f"Settings '{name}' not found in registry.")
        return SettingsRegistry._settings[name]

from performance_configurator import PerformanceConfigurator
from config_manager import ConfigManager

# Register settings instances
SettingsRegistry.register_settings("config_manager", ConfigManager("config.yaml"))
SettingsRegistry.register_settings("performance_configurator", PerformanceConfigurator(performance_tracker))
config_manager = SettingsRegistry.get_settings("config_manager")
performance_configurator = SettingsRegistry.get_settings("performance_configurator")
