from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer
import pendulum

class TimestampFormatter:
    @staticmethod
    @inject
    def format(seconds: int, logger=Provide[AppContainer.logger]) -> str:
        """
        Formats seconds into a human-readable HH:MM:SS format using pendulum.

        Args:
            seconds (int): Total time in seconds.

        Returns:
            str: Formatted time as HH:MM:SS.
        """
        try:
            if seconds < 0:
                raise ValueError("Seconds cannot be negative")

            duration = pendulum.duration(seconds=seconds)
            formatted_time = duration.format("HH:mm:ss", formatter="alternative")
            logger.info(f"Formatted timestamp: {formatted_time}")
            return formatted_time
        except Exception as e:
            logger.error(f"Failed to format timestamp: {e}")
            raise

# Example usage with dependency injection wiring:
if __name__ == "__main__":
    from infrastructure.dependency_setup import container

    container.wire(modules=[__name__])
    formatter = TimestampFormatter()
    print(formatter.format(3661))  # Expected output: "01:01:01"
