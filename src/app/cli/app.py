import click
from dependency_injector.wiring import Provide, inject

from src.app.cli import cli_audio, cli_download, cli_text, cli_transcription
from src.infrastructure.app.app_container import AppContainer


class CommandManager:
    """Manages the registration and execution of commands."""

    def __init__(self, logger):
        self.commands = {}
        self.logger = logger

    def register(self, name: str, command: click.Command):
        """Register a command."""
        if name in self.commands:
            raise ValueError(f"Command '{name}' is already registered.")
        self.commands[name] = command
        self.logger.info(f"Command '{name}' registered successfully.")

    def execute(self, name: str, *args, **kwargs):
        """Execute a registered command."""
        if name not in self.commands:
            self.logger.error(f"Command '{name}' not found.")
            raise ValueError(f"Command '{name}' not found.")
        self.logger.info(f"Executing command '{name}'")
        return self.commands[name].main(*args, **kwargs)

    def list_commands(self):
        """List all registered commands."""
        self.logger.info("Listing all registered commands.")
        return list(self.commands.keys())

    def register_to_cli(self, cli: click.Group):
        """Register all commands with a Click group."""
        for name, command in self.commands.items():
            cli.add_command(command, name=name)
        self.logger.info("All commands registered to the CLI.")


@click.group()
@inject
def cli(logger=Provide[AppContainer.logger]):
    """Unified CLI for managing various tasks."""
    logger.info("CLI initialized.")


@inject
def discover_and_register_commands(command_manager: CommandManager):
    """
    Discover and register all commands dynamically from CLI modules.
    """
    # Example: Discover commands from each module
    command_manager.register("audio_processing", cli_audio.cli)
    command_manager.register("text_processing", cli_text.cli)
    command_manager.register("download", cli_download.cli)
    command_manager.register("transcription", cli_transcription.cli)


if __name__ == "__main__":
    # Dependency injection setup
    container = AppContainer()
    container.wire(
        modules=[
            "src.cli.cli_audio",
            "src.cli.cli_text",
            "src.cli.cli_download",
            "src.cli.cli_transcription",
        ]
    )

    # Initialize logger and performance tracker
    logger = container.logger()
    performance_tracker = container.performance_tracker()

    # Initialize Command Manager
    command_manager = CommandManager(logger=logger)

    # Discover and register commands
    with performance_tracker.track_execution("Command Registration"):
        discover_and_register_commands(command_manager)

    # Register commands dynamically with the Click CLI
    command_manager.register_to_cli(cli)

    # Run the CLI
    try:
        cli()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
