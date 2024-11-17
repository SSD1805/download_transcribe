class PerformanceConfigurator:
    def __init__(self, performance_tracker):
        self.performance_tracker = performance_tracker

    def configure(self, performance_settings):
        monitor_interval = performance_settings.get("monitor_interval", 5)
        self.performance_tracker.monitor_memory_usage(interval=monitor_interval)
        logger.info(f"Performance tracker configured with interval: {monitor_interval} seconds")
