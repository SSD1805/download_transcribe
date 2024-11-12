import unittest
from src.utils.timestamp_formatter import TimestampFormatter

class TestTimestampFormatter(unittest.TestCase):
    def test_format_timestamp(self):
        self.assertEqual(TimestampFormatter.format_timestamp(3661), "01:01:01")
        self.assertEqual(TimestampFormatter.format_timestamp(0), "00:00:00")
        self.assertEqual(TimestampFormatter.format_timestamp(59), "00:00:59")
        self.assertEqual(TimestampFormatter.format_timestamp(3600), "01:00:00")
        self.assertEqual(TimestampFormatter.format_timestamp(86399), "23:59:59")

if __name__ == '__main__':
    unittest.main()


#this test passed successfully