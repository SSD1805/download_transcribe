import click
from dependency_injector.wiring import Provide, inject
from src.infrastructure.app.app_container import AppContainer


class BaseCommand(click.Command):
    """
    A base class for CLI commands that injects logging and performance tracking
    from the AppContainer.
    """

    @inject
    def __init__(self, *args, logger=Provide[AppContainer.logger], tracker=Provide[AppContainer.performance_tracker], **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.performance_tracker = tracker

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
