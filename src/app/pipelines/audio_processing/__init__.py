# Define public API for the audio_processing module
__all__ = [
    "AudioSplitter",
    "AudioConverter",
    "AudioNormalizer",
    "AudioTrimmer",
    "AudioProcessorBase",
]

# Mapping of class names to their respective modules for lazy loading
_module_map = {
    "AudioSplitter": "audio_splitter",
    "AudioConverter": "audio_converter",
    "AudioNormalizer": "audio_normalizer",
    "AudioTrimmer": "audio_trimmer",
    "AudioProcessorBase": "audioprocessorbase",
}


def __getattr__(name):
    """Lazy loading of submodules to avoid circular imports."""
    if name in __all__:
        module_name = _module_map.get(name)
        if module_name:
            try:
                # Dynamically import the module and return the attribute
                module = __import__(f"{__name__}.{module_name}", fromlist=[name])
                return getattr(module, name)
            except ImportError as e:
                raise ImportError(
                    f"Failed to import '{name}' from submodule '{module_name}': {e}"
                )
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")
