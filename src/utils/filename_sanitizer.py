# filename_sanitizer.py
import re

class FilenameSanitizer:
    @staticmethod
    def sanitize_filename(filename):
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return sanitized_name