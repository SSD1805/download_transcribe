class BatchProcessorFactory:
    """
    Factory to generate the correct batch processor based on type.
    """
    _processors = {}

    @staticmethod
    def register_processor(data_type, processor_class):
        """
        Register a new processor class for a specific data type.
        """
        BatchProcessorFactory._processors[data_type] = processor_class

    @staticmethod
    def get_processor(data_type, batch_size=10, use_threads=False):
        """
        Retrieve the appropriate processor class for the given data type.

        Args:
            data_type (str): The type of data to process (e.g., 'audio', 'text').
            batch_size (int): The batch size.
            use_threads (bool): Whether to use threading for concurrency.

        Returns:
            BatchProcessor: An instance of the requested processor class.
        """
        processor_class = BatchProcessorFactory._processors.get(data_type)
        if not processor_class:
            raise ValueError(f"Unsupported data type: {data_type}")
        return processor_class(batch_size=batch_size, use_threads=use_threads)


# Register available processors
from src.core.batch_processor import AudioBatchProcessor, TextBatchProcessor

BatchProcessorFactory.register_processor("audio", AudioBatchProcessor)
BatchProcessorFactory.register_processor("text", TextBatchProcessor)
