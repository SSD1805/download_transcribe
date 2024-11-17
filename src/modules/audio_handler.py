# src/pipelines/audio/audio_handler.py
class AudioHandler:
    """
    Audio handler that uses a registry to retrieve pre-configured handlers.
    """
    def handle_audio(self, operation_name, **kwargs):
        """
        Handle an audio operation by delegating to the appropriate handler.

        Args:
            operation_name (str): The operation to perform (e.g., 'convert', 'normalize').
            **kwargs: Arguments required by the handler.

        Returns:
            Result of the handler's operation.
        """
        handler = AudioHandlerRegistry.get_handler(operation_name)
        return handler.process(**kwargs)

audio_handler = AudioHandler()

# Convert audio
audio_handler.handle_audio("convert", input_file="input.mp3", output_file="output.wav", target_format="wav")

# Normalize audio
audio_handler.handle_audio("normalize", input_file="input.wav", output_file="normalized.wav")

# Split audio
audio_handler.handle_audio("split", input_file="input.wav", chunk_duration_ms=30000, output_file_prefix="chunk_")

# Trim audio
audio_handler.handle_audio("trim", input_file="input.wav", output_file="trimmed.wav", silence_thresh=-40)
