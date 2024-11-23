import os

from src.app.pipelines.transcription.basepipeline import BasePipeline


class TranscriptionManager(BasePipeline):
    """
    Coordinates the transcription process for a batch of audio files.
    """

    def __init__(self, input_directory: str, output_directory: str, transcriber, saver):
        super().__init__()
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.transcriber = transcriber
        self.saver = saver

    def process_files(self):
        """
        Processes multiple audio files for transcription.
        """
        self.ensure_directory_exists(self.output_directory)
        audio_files = self.get_files_with_extensions(self.input_directory, (".wav", ".mp3"))
        for file_name in audio_files:
            self._process_file(file_name)

    def _process_file(self, file_name: str):
        """
        Transcribes and saves a single file.
        """
        input_path = os.path.join(self.input_directory, file_name)

        with self.track(f"Transcribing {file_name}"):
            segments = self.transcriber.transcribe(input_path)
            self.saver.save_transcription(segments, file_name)
            self.logger.info(f"Transcription completed for '{file_name}'.")
