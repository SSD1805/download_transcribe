import unittest
import os
from src.audio_pipeline.audio_converter import AudioConverter

class TestAudioConverter(unittest.TestCase):
    def setUp(self):
        self.input_directory = '/app/audio_files'
        self.output_directory = '/app/processed_audio'
        self.format = 'wav'
        self.converter = AudioConverter(self.input_directory, self.output_directory, self.format)
        os.makedirs(self.input_directory, exist_ok=True)
        os.makedirs(self.output_directory, exist_ok=True)

    def tearDown(self):
        for f in os.listdir(self.input_directory):
            os.remove(os.path.join(self.input_directory, f))
        for f in os.listdir(self.output_directory):
            os.remove(os.path.join(self.output_directory, f))

    def test_convert_audio_format(self):
        input_file = os.path.join(self.input_directory, 'example.mp3')
        with open(input_file, 'wb') as f:
            f.write(b'\x00\x00\x00\x00')  # Dummy file content
        output_file = self.converter.convert_audio_format(input_file)
        self.assertTrue(os.path.exists(output_file))

    def test_batch_convert_audio_files(self):
        input_file = os.path.join(self.input_directory, 'example.mp3')
        with open(input_file, 'wb') as f:
            f.write(b'\x00\x00\x00\x00')  # Dummy file content
        self.converter.batch_convert_audio_files()
        output_file = os.path.join(self.output_directory, 'example.wav')
        self.assertTrue(os.path.exists(output_file))

if __name__ == '__main__':
    unittest.main()