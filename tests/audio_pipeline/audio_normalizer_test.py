import unittest
import os
from unittest.mock import patch, MagicMock
from pydub import AudioSegment
from src.audio_pipeline.audio_normalizer import AudioNormalizer

class TestAudioNormalizer(unittest.TestCase):
    def setUp(self):
        self.output_directory = '/app/processed_audio'
        self.format = 'wav'
        self.normalizer = AudioNormalizer(self.output_directory, self.format)
        os.makedirs(self.output_directory, exist_ok=True)

    def tearDown(self):
        for f in os.listdir(self.output_directory):
            os.remove(os.path.join(self.output_directory, f))

    @patch('src.downloaders.audio_normalizer.AudioSegment')
    @patch('src.downloaders.audio_normalizer.logger')
    def test_normalize(self, mock_logger, mock_audio_segment):
        input_file = 'test.mp3'
        mock_audio = MagicMock(spec=AudioSegment)
        mock_audio_segment.from_file.return_value = mock_audio
        mock_audio.export.return_value = None

        output_file = self.normalizer.normalize(input_file)

        mock_audio_segment.from_file.assert_called_once_with(input_file)
        mock_audio.export.assert_called_once_with(os.path.join(self.output_directory, 'test_normalized.wav'), format=self.format)
        mock_logger.info.assert_any_call(f"Normalized audio saved as {os.path.join(self.output_directory, 'test_normalized.wav')}")
        self.assertEqual(output_file, os.path.join(self.output_directory, 'test_normalized.wav'))

if __name__ == '__main__':
    unittest.main()

# this test needs to be completed