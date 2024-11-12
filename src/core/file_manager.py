import os
import pandas as pd
from tqdm import tqdm
from logger_manager import LoggerManager
from file_uploader import FileUploader  # Import the FileUploader

log_manager = LoggerManager()
logger = log_manager.get_logger()


class FileManager:
    def __init__(self):
        self.uploader = FileUploader()  # Create an instance of FileUploader

    @staticmethod
    def sanitize_filename(title):
        return ''.join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in title)

    @staticmethod
    def ensure_directories_exist(*directories):
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Created directory: {directory}")

    def files_exist(self, title, podcast_audio_dir, transcriptions_dir):
        sanitized_title = self.sanitize_filename(title)
        audio_file = os.path.join(podcast_audio_dir, f'{sanitized_title}.mp3')
        transcription_file = os.path.join(transcriptions_dir, f'{sanitized_title}.txt')
        audio_exists = os.path.exists(audio_file)
        transcription_exists = os.path.exists(transcription_file)
        logger.info(f"Audio file exists: {audio_exists}, Transcription file exists: {transcription_exists}")
        return audio_exists, transcription_exists

    @staticmethod
    def list_files_with_progress(directory):
        files = []
        for file in tqdm(os.listdir(directory), desc="Listing files"):
            files.append(file)
        logger.info(f"Listed {len(files)} files in directory: {directory}")
        return files

    def save_file_metadata_to_csv(self, directory, output_csv):
        files = self.list_files_with_progress(directory)
        metadata = [{"file_name": file, "size": os.path.getsize(os.path.join(directory, file))} for file in files]
        df = pd.DataFrame(metadata)
        df.to_csv(output_csv, index=False, encoding="utf-8")
        logger.info(f"Saved file metadata to CSV: {output_csv}")

    def upload_file_chunk(self, data, target_directory, lock_id):
        """
        Use FileUploader to handle chunked file uploads.

        Args:
            data (dict): Chunk data including directory, fileName, chunk, and isLastChunk.
            target_directory (str): Target directory to save the complete file.
            lock_id (str): Unique ID for managing chunk upload locks.

        Returns:
            dict: Status message from FileUploader.
        """
        # Delegate upload responsibility to FileUploader
        return self.uploader.handle_chunk(data, target_directory, lock_id)
