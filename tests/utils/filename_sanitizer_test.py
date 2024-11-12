import unittest
from src.utils.filename_sanitizer import FilenameSanitizer

class TestFilenameSanitizer(unittest.TestCase):
    def test_sanitize_filename(self):
        self.assertEqual(FilenameSanitizer.sanitize_filename("file<name>.txt"), "file_name_.txt")
        self.assertEqual(FilenameSanitizer.sanitize_filename("file:name.txt"), "file_name.txt")
        self.assertEqual(FilenameSanitizer.sanitize_filename("file/name.txt"), "file_name.txt")
        self.assertEqual(FilenameSanitizer.sanitize_filename("file\\name.txt"), "file_name.txt")
        self.assertEqual(FilenameSanitizer.sanitize_filename("file|name.txt"), "file_name.txt")
        self.assertEqual(FilenameSanitizer.sanitize_filename("file?name.txt"), "file_name.txt")
        self.assertEqual(FilenameSanitizer.sanitize_filename("file*name.txt"), "file_name.txt")

if __name__ == '__main__':
    unittest.main()

#this test passed successfully