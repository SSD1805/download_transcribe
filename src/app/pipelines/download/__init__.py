__all__ = ["DownloadPipeline"]


def __getattr__(name):
    """Lazy loading of the DownloadPipeline class."""
    if name in __all__:
        try:
            module = __import__(f"{__name__}.download_pipeline", fromlist=[name])
            return getattr(module, name)
        except ImportError as e:
            raise ImportError(f"Failed to import '{name}' from 'download_pipeline': {e}")
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")
