import os

from src.app.pipelines.transcription.basepipeline import BasePipeline


class AudioProcessingPipeline(BasePipeline):
    """
    Manages the audio processing pipeline, coordinating conversion, transcription,
    and saving results.
    """

    def __init__(self, input_directory: str, output_directory: str, converter, transcriber, saver):
        super().__init__()
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.converter = converter
        self.transcriber = transcriber
        self.saver = saver

    def process_files(self):
        """
        Orchestrates the processing of multiple audio files.
        """
        self.ensure_directory_exists(self.output_directory)
        audio_files = self.get_files_with_extensions(self.input_directory, (".mp3", ".wav", ".m4a", ".flac"))
        for file_name in audio_files:
            self._process_single_file(file_name)

    def _process_single_file(self, file_name: str):
        """
        Processes a single audio file.
        """
        input_path = os.path.join(self.input_directory, file_name)

        with self.track(f"Processing {file_name}"):
            if not file_name.endswith(".wav"):
                wav_file = self.converter.convert_to_wav(input_path)
                if not wav_file:
                    self.logger.warning(f"Skipping '{file_name}' due to conversion error.")
                    return
            else:
                wav_file = input_path

            segments = self.transcriber.transcribe(wav_file)
            self.saver.save_transcription(segments, file_name)
            self.logger.info(f"Successfully processed '{file_name}'.")
