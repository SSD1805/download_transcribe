import unittest
from unittest.mock import patch, MagicMock
from src.audio_transcriber import AudioTranscriber

class TestAudioTranscriber(unittest.TestCase):
    def setUp(self):
        self.transcriber = AudioTranscriber()

    @patch('src.audio_transcriber.whisperx.load_model')
    @patch('src.audio_transcriber.whisper.load_model')
    def test_load_models(self, mock_whisper_load_model, mock_whisperx_load_model):
        mock_whisperx_load_model.return_value = MagicMock()
        mock_whisper_load_model.return_value = MagicMock()

        transcriber = AudioTranscriber()
        self.assertIsNotNone(transcriber.whisperx_model)
        self.assertIsNotNone(transcriber.whisper_model)

    @patch('src.audio_transcriber.whisperx.load_model')
    @patch('src.audio_transcriber.whisper.load_model')
    def test_transcribe_with_whisperx(self, mock_whisper_load_model, mock_whisperx_load_model):
        mock_whisperx_model = MagicMock()
        mock_whisperx_model.transcribe.return_value = {'segments': [{'text': 'test transcription'}]}
        mock_whisperx_load_model.return_value = mock_whisperx_model
        mock_whisper_load_model.return_value = MagicMock()

        transcriber = AudioTranscriber()
        result = transcriber.transcribe('test_audio.mp3', use_whisperx=True)
        self.assertEqual(result, [{'text': 'test transcription'}])

    @patch('src.audio_transcriber.whisperx.load_model')
    @patch('src.audio_transcriber.whisper.load_model')
    def test_transcribe_with_whisper(self, mock_whisper_load_model, mock_whisperx_load_model):
        mock_whisper_model = MagicMock()
        mock_whisper_model.transcribe.return_value = {'text': 'test transcription'}
        mock_whisper_load_model.return_value = mock_whisper_model
        mock_whisperx_load_model.return_value = None

        transcriber = AudioTranscriber()
        result = transcriber.transcribe('test_audio.mp3', use_whisperx=False)
        self.assertEqual(result, [{'text': 'test transcription'}])

if __name__ == '__main__':
    unittest.main()