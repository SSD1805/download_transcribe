class AudioHandlerRegistry:
    """
    Registry to store and retrieve pre-configured audio handlers.
    """
    _handlers = {}

    @staticmethod
    def register_handler(operation_name, handler_instance):
        """
        Register an existing handler instance for a specific operation.

        Args:
            operation_name (str): The operation name (e.g., 'convert', 'normalize').
            handler_instance (object): The handler instance to register.
        """
        AudioHandlerRegistry._handlers[operation_name] = handler_instance

    @staticmethod
    def get_handler(operation_name):
        """
        Retrieve the handler instance for the specified operation.

        Args:
            operation_name (str): The operation name (e.g., 'convert', 'normalize').

        Returns:
            object: The handler instance.

        Raises:
            ValueError: If the operation is not registered.
        """
        handler = AudioHandlerRegistry._handlers.get(operation_name)
        if not handler:
            raise ValueError(f"No handler registered for operation: {operation_name}")
        return handler

# Register audio handlers with shared dependencies
from src.pipelines.audio.audio_converter import AudioConverter
from src.pipelines.audio.audio_normalizer import AudioNormalizer
from src.pipelines.audio.audio_splitter import AudioSplitter
from src.pipelines.audio.audio_trimmer import AudioTrimmer

AudioHandlerRegistry.register_handler("convert", AudioConverter(output_directory="/data/output", format="wav"))
AudioHandlerRegistry.register_handler("normalize", AudioNormalizer(output_directory="/data/output", format="wav"))
AudioHandlerRegistry.register_handler("split", AudioSplitter(output_directory="/data/output", format="wav"))
AudioHandlerRegistry.register_handler("trim", AudioTrimmer(output_directory="/data/output", format="wav"))
