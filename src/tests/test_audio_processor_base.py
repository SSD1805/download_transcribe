from unittest import TestCase
from unittest.mock import MagicMock, patch
from pydub import AudioSegment
import os

from src.app.pipelines.audio_processing.audio_processor_base import AudioProcessorBase


class TestAudioProcessor(AudioProcessorBase):
    """
    A concrete implementation of AudioProcessorBase for testing purposes.
    """
    def process(self, input_file: str, *args, **kwargs) -> str:
        """Mock implementation of the abstract process method."""
        return f"Processed {input_file}"


class TestAudioProcessorBase(TestCase):
    """
    Unit tests for AudioProcessorBase functionality using TestAudioProcessor.
    """

    @patch('os.makedirs')
    def setUp(self, mock_makedirs):
        self.mock_logger = MagicMock()
        self.mock_tracker = MagicMock()
        self.processor = TestAudioProcessor(
            output_directory='/fake/dir',
            logger=self.mock_logger,
            tracker=self.mock_tracker,
            format='wav'
        )

    @patch('pydub.AudioSegment.from_file')
    def test_load_audio_success(self, mock_from_file):
        """Test successful loading of an audio file."""
        mock_audio = MagicMock(spec=AudioSegment)
        mock_from_file.return_value = mock_audio

        result = self.processor.load_audio('input.mp3')
        self.assertEqual(result, mock_audio, "Audio file should load correctly.")
        self.mock_logger.info.assert_called_once_with("Loading audio file: input.mp3")

    @patch('pydub.AudioSegment.from_file')
    def test_load_audio_failure(self, mock_from_file):
        """Test failure to load an audio file."""
        mock_from_file.side_effect = Exception("File not found")

        with self.assertRaises(RuntimeError, msg="Loading a non-existent file should raise RuntimeError."):
            self.processor.load_audio('input.mp3')
        self.mock_logger.error.assert_called_once()

    @patch('pydub.AudioSegment.from_file')
    def test_load_audio_empty_file(self, mock_from_file):
        """Test loading an empty file path."""
        with self.assertRaises(ValueError, msg="Empty file path should raise ValueError."):
            self.processor.load_audio('')

    @patch('pydub.AudioSegment.export')
    def test_save_audio_success(self, mock_export):
        """Test successful saving of an audio file."""
        mock_audio = MagicMock(spec=AudioSegment)
        mock_export.return_value = None

        result = self.processor.save_audio(mock_audio, 'output.wav')
        self.assertEqual(result, '/fake/dir/output.wav', "Audio file should save to the expected path.")
        self.mock_logger.info.assert_called_once_with("Saving audio to /fake/dir/output.wav")
        self.mock_tracker.track_execution.assert_called_once_with("save_audio", {"file": "/fake/dir/output.wav"})

    @patch('pydub.AudioSegment.export')
    def test_save_audio_failure(self, mock_export):
        """Test failure to save an audio file."""
        mock_audio = MagicMock(spec=AudioSegment)
        mock_export.side_effect = Exception("Export error")

        with self.assertRaises(RuntimeError, msg="Failure to save audio should raise RuntimeError."):
            self.processor.save_audio(mock_audio, 'output.wav')
        self.mock_logger.error.assert_called_once()

    @patch('os.makedirs', side_effect=FileNotFoundError("Output directory not found"))
    def test_save_audio_missing_output_directory(self, mock_makedirs):
        """Test saving audio when the output directory is missing."""
        mock_audio = MagicMock(spec=AudioSegment)
        with self.assertRaises(RuntimeError, msg="Saving to a missing output directory should raise RuntimeError."):
            self.processor.save_audio(mock_audio, 'output.wav')
        self.mock_logger.error.assert_called_once()

    def test_process_method(self):
        """Test the concrete implementation of the abstract `process` method."""
        result = self.processor.process('input.mp3')
        self.assertEqual(result, "Processed input.mp3", "The process method should return the expected result.")
