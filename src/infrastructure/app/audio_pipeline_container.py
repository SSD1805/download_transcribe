from dependency_injector import containers, providers
from src.app.pipelines.audio_processing import (
    AudioConverter,
    AudioNormalizer,
    AudioSplitter,
    AudioTrimmer,
    AudioProcessingPipeline,
)


class AudioPipelineContainer(containers.DeclarativeContainer):
    logger = providers.Dependency()
    tracker = providers.Dependency()

    # Audio components
    audio_converter = providers.Singleton(AudioConverter)
    audio_normalizer = providers.Singleton(AudioNormalizer)
    audio_splitter = providers.Singleton(AudioSplitter)
    audio_trimmer = providers.Singleton(AudioTrimmer)

    # Audio processing pipeline
    audio_processing_pipeline = providers.Singleton(
        AudioProcessingPipeline,
        converter=audio_converter,
        normalizer=audio_normalizer,
        splitter=audio_splitter,
        trimmer=audio_trimmer,
    )
