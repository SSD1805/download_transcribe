from src.pipelines.base_pipeline import BasePipeline


class TranscriptionManager(BasePipeline):
    """
    Handles transcription of audio files and saving the results.
    """

    def __init__(self, input_directory: str, output_directory: str, transcriber, saver):
        super().__init__()
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.transcriber = transcriber
        self.saver = saver

    def process_files(self):
        self.ensure_directory_exists(self.output_directory)
        audio_files = self.get_files_with_extensions(self.input_directory, (".wav", ".mp3"))
        for file_name in audio_files:
            self._process_file(file_name)

    def _process_file(self, file_name: str):
        """
        Transcribe and save a single file.
        """
        input_path = os.path.join(self.input_directory, file_name)
        segments = self.transcriber.transcribe(input_path)
        self.saver.save_transcription(segments, file_name)
        self.logger.info(f"Transcription completed for '{file_name}'.")
