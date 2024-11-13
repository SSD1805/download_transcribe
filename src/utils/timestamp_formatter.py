# timestamp_formatter_test.py
class TimestampFormatter:
    @staticmethod
    def format_timestamp(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        sec = int(seconds % 60)
        formatted_time = f"{hours:02}:{minutes:02}:{sec:02}"
        return formatted_time