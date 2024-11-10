import whisper
import os
import datetime
from logger import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

class Transcriber:
    def __init__(self, model_size='base'):
        """
        Initialize the Transcriber with a specified Whisper model size.

        Args:
            model_size (str): The size of the Whisper model to load (e.g., 'base', 'small', 'large').
        """
        self.model_size = model_size
        logger.info(f"Loading Whisper model: {self.model_size}")
        self.whisper_model = whisper.load_model(model_size)
        self.input_audio_path = ""
        self.transcription_output_path = ""

    def load_audio(self, audio_path):
        """
        Load the audio file for transcription.

        Args:
            audio_path (str): Path to the audio file to be transcribed.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at path: {audio_path}")

        self.input_audio_path = audio_path
        logger.info(f"Audio file loaded: {audio_path}")

    def transcribe_audio(self):
        """
        Transcribe the loaded audio file using the Whisper model.

        Returns:
            dict: The transcription result including text and timestamps.
        """
        if not self.input_audio_path:
            raise ValueError("No audio file loaded for transcription.")

        logger.info("Starting transcription...")
        transcription = self.whisper_model.transcribe(self.input_audio_path)
        logger.info("Transcription completed.")
        return transcription

    def save_transcription(self, transcription, filepath, format='txt'):
        """
        Save the transcription result to a file.

        Args:
            transcription (dict): The transcription result.
            filepath (str): The path to save the transcription file.
            format (str): The format to save the file (e.g., 'txt' or 'csv').
        """
        self.transcription_output_path = filepath

        if format == 'txt':
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(transcription['text'])
            logger.info(f"Transcription saved as text file: {filepath}")

        elif format == 'csv':
            import pandas as pd
            segments = transcription['segments']
            df = pd.DataFrame(segments)
            df.to_csv(filepath, index=False)
            logger.info(f"Transcription saved as CSV file: {filepath}")

        else:
            raise ValueError("Unsupported format. Please use 'txt' or 'csv'.")

    def format_transcription(self, transcription):
        """
        Format the transcription result for better readability.

        Args:
            transcription (dict): The transcription result.

        Returns:
            str: Formatted transcription text.
        """
        formatted_text = ""
        for segment in transcription['segments']:
            start_time = str(datetime.timedelta(seconds=int(segment['start'])))
            end_time = str(datetime.timedelta(seconds=int(segment['end'])))
            text = segment['text']
            formatted_text += f"[{start_time} - {end_time}] {text}\n"

        return formatted_text