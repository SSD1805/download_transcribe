from dask.distributed import Client, WorkerPlugin
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app.app_container import AppContainer


class PerformanceMonitoringPlugin(WorkerPlugin):
    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.logger],
        performance_tracker=Provide[AppContainer.performance_tracker],
        interval=5,
    ):
        """
        Initialize the performance monitoring plugin.

        Args:
            logger: The logger instance.
            performance_tracker: The performance tracker instance.
            interval (int): The interval for performance tracking.
        """
        self.logger = logger
        self.performance_tracker = performance_tracker
        self.interval = interval

    def setup(self, worker):
        """
        This method is called when the worker starts.
        It will begin memory usage monitoring.
        """
        self.logger.info("Starting performance monitoring on worker...")
        self.performance_tracker.monitor_memory_usage(interval=self.interval)

    def teardown(self, worker):
        """
        This method is called when the worker stops.
        It will stop memory usage monitoring.
        """
        self.logger.info("Stopping performance monitoring on worker...")
        self.performance_tracker.stop_memory_monitoring()


# Register the plugin with the Dask client
client = Client()
client.register_worker_plugin(PerformanceMonitoringPlugin(interval=5))

if __name__ == "__main__":
    # Wire the dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])

    # Example: Run performance monitoring manually if needed
    client.run(lambda: PerformanceMonitoringPlugin().setup(worker=None))
