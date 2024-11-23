import click
from dependency_injector.wiring import Provide, inject
from src.infrastructure.app.app_container import AppContainer


class BaseCommand(click.Command):
    """
    A base class for CLI commands that injects logging, performance tracking,
    and shared services from the AppContainer.
    """

    @inject
    def __init__(
        self,
        *args,
        logger=Provide[AppContainer.logger],
        tracker=Provide[AppContainer.performance_tracker],
        audio_processor=Provide[AppContainer.audio_processor],
        downloader=Provide[AppContainer.downloader],
        transcription_pipeline=Provide[AppContainer.transcription_pipeline],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.performance_tracker = tracker
        self.audio_processor = audio_processor
        self.downloader = downloader
        self.transcription_pipeline = transcription_pipeline

    def invoke(self, ctx):
        """Override Click's invoke to include performance tracking."""
        command_name = ctx.command.name
        self.logger.info(f"Executing command: {command_name}")
        with self.performance_tracker.track_execution(f"CLI Command: {command_name}"):
            try:
                return super().invoke(ctx)
            except Exception as e:
                self.logger.error(f"Error in command '{command_name}': {e}")
                raise
