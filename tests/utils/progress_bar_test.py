import unittest
from unittest.mock import patch
from src.utils.progress_bar import ProgressBar

class TestProgressBar(unittest.TestCase):
    @patch('src.utils.progress_bar.tqdm')
    def test_progress_bar(self, mock_tqdm):
        iterable = range(10)
        description = "Test Progress"

        result = ProgressBar.progress_bar(iterable, description)

        mock_tqdm.assert_called_once_with(iterable, desc=description)
        self.assertEqual(result, mock_tqdm.return_value)

if __name__ == '__main__':
    unittest.main()

#this test needs to be completed