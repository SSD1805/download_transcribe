import os
import logging
from transcriber import Transcriber
from logger import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

class TranscriptionManager:
    def __init__(self, audio_directory, transcriptions_directory, log_path='transcription.log', format='txt'):
        """
        Initialize the TranscriptionManager with specified directories and settings.

        Args:
            audio_directory (str): Path to the directory containing audio files.
            transcriptions_directory (str): Path to the directory for saving transcriptions.
            log_path (str): Path to the log file for recording transcription activity.
            format (str): Default format for transcription output (e.g., 'txt' or 'csv').
        """
        self.audio_directory = audio_directory
        self.transcriptions_directory = transcriptions_directory
        self.transcriber = Transcriber(model_size='base')
        self.format = format

        # Configure logging
        self.log_path = log_path
        logging.basicConfig(filename=self.log_path, level=logging.INFO, format='%(asctime)s - %(message)s')
        print("TranscriptionManager initialized.")

    def list_audio_files(self):
        """
        List all audio files in the audio directory.

        Returns:
            list: List of audio file paths.
        """
        if not os.path.exists(self.audio_directory):
            raise FileNotFoundError(f"Audio directory not found: {self.audio_directory}")

        audio_files = [os.path.join(self.audio_directory, f) for f in os.listdir(self.audio_directory)
                       if f.lower().endswith(('.mp3', '.wav', '.flac'))]

        if not audio_files:
            print("No audio files found in the directory.")
        else:
            print(f"Found {len(audio_files)} audio files.")

        return audio_files

    def transcribe_all(self):
        """
        Transcribe all audio files in the directory and save the results.
        """
        audio_files = self.list_audio_files()

        for audio_file in audio_files:
            try:
                print(f"Transcribing file: {audio_file}")
                self.transcriber.load_audio(audio_file)
                transcription = self.transcriber.transcribe_audio()

                # Generate output path and save transcription
                output_path = self.get_transcription_output_path(audio_file)
                self.transcriber.save_transcription(transcription, output_path, format=self.format)
                self.log_transcription_activity(audio_file, "Success")

            except Exception as e:
                print(f"Error transcribing {audio_file}: {e}")
                self.log_transcription_activity(audio_file, f"Failed: {e}")

    def get_transcription_output_path(self, audio_file):
        """
        Generate the output path for saving the transcription.

        Args:
            audio_file (str): Path to the input audio file.

        Returns:
            str: Path to the output transcription file.
        """
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_file = f"{base_name}_transcription.{self.format}"
        output_path = os.path.join(self.transcriptions_directory, output_file)
        print(f"Generated output path: {output_path}")
        return output_path

    def log_transcription_activity(self, audio_file, status):
        """
        Log the transcription activity to a log file.

        Args:
            audio_file (str): Name of the audio file being transcribed.
            status (str): The status of the transcription (e.g., 'Success', 'Failed').
        """
        logging.info(f"{audio_file} - {status}")
        print(f"Logged activity for {audio_file}: {status}")