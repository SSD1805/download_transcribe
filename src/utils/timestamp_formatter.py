class TimestampFormatter:
    @staticmethod
    def format(seconds: int) -> str:
        """
        Formats seconds into a human-readable HH:MM:SS format.

        Args:
            seconds (int): Total time in seconds.

        Returns:
            str: Formatted time as HH:MM:SS.
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        sec = seconds % 60
        formatted_time = f"{hours:02}:{minutes:02}:{sec:02}"
        logger.info(f"Formatted timestamp: {formatted_time}")
        return formatted_time
