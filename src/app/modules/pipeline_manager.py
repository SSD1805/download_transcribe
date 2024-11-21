from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer


class PipelineManager:
    @inject
    def __init__(
        self,
        config_manager=Provide[AppContainer.configuration_registry],
        logger=Provide[AppContainer.logger],
        performance_tracker=Provide[AppContainer.performance_tracker],
        memory_monitor=Provide[AppContainer.memory_monitor],
        batch_processor_factory=Provide[AppContainer.batch_processor],
    ):
        self.config_manager = config_manager
        self.logger = logger
        self.performance_tracker = performance_tracker
        self.memory_monitor = memory_monitor

        batch_size = self.config_manager.get("batch_size", 5)  # Default batch size
        self.batch_processor = batch_processor_factory(batch_size=batch_size)

        self.logger.info(
            "PipelineManager initialized with batch size and memory monitoring."
        )

    def process_batch(self, func, items):
        """
        Processes a batch of items using the provided function.

        Args:
            func (callable): Function to process each item.
            items (iterable): Items to process in batches.
        """
        with self.performance_tracker.track_execution("Batch Processing"):
            self.batch_processor.process(func, items)
            self.logger.info("Batch processing completed.")
