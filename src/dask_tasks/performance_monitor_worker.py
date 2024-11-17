from dask.distributed import Client, WorkerPlugin
from src.core.services import CoreServices

# Get logger and performance tracker from CoreServices
logger = CoreServices.get_logger()
perf_tracker = CoreServices.get_performance_tracker()


# Initialize Dask client and logger
client = Client()

class PerformanceMonitoringPlugin(WorkerPlugin):
    def __init__(self, interval=5):
        self.performance_tracker = PerformanceTracker()
        self.interval = interval

    def setup(self, worker):
        """
        This method is called when the worker starts.
        It will begin memory usage monitoring.
        """
        logger.info("Starting performance monitoring on worker...")
        self.performance_tracker.monitor_memory_usage(interval=self.interval)

    def teardown(self, worker):
        """
        This method is called when the worker stops.
        It will stop memory usage monitoring.
        """
        logger.info("Stopping performance monitoring on worker...")
        self.performance_tracker.stop_memory_monitoring()

# Register the plugin with the Dask client
client.register_worker_plugin(PerformanceMonitoringPlugin(interval=5))

if __name__ == "__main__":
    # Example to run monitoring manually if needed
    client.run(lambda: PerformanceMonitoringPlugin().setup(worker=None))
