from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Abstract Base Command class to define a uniform interface for all commands.
    """

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the command with given arguments.
        """
        pass
