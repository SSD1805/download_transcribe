import os
from tqdm import tqdm
from src.pipelines.audio.audio_converter import AudioConverter
from src.pipelines.transcription.audio_transcriber import AudioTranscriber
from src.pipelines.transcription.transcription_saver import TranscriptionSaver
from src.core.services import CoreServices


class AudioProcessingPipeline:
    def __init__(self, input_directory, output_directory, converter=None, transcriber=None, saver=None):
        """
        Initialize the audio processing pipeline.

        Args:
            input_directory (str): Directory containing input audio files.
            output_directory (str): Directory to save transcriptions.
            converter (AudioConverter, optional): AudioConverter instance.
            transcriber (AudioTranscriber, optional): AudioTranscriber instance.
            saver (TranscriptionSaver, optional): TranscriptionSaver instance.
        """
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.logger = CoreServices.get_logger()
        self.perf_tracker = CoreServices.get_performance_tracker()

        self.converter = converter or AudioConverter(output_directory=output_directory)
        self.transcriber = transcriber or AudioTranscriber()
        self.saver = saver or TranscriptionSaver(output_directory=output_directory)

    def process_files(self):
        """
        Process audio files: convert to WAV, transcribe, and save results.
        """
        with self.perf_tracker.track_execution("Audio Processing Pipeline"):
            if not os.path.exists(self.input_directory):
                self.logger.error(f"Input directory '{self.input_directory}' does not exist.")
                return

            audio_files = [
                f for f in os.listdir(self.input_directory)
                if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))
            ]

            if not audio_files:
                self.logger.warning(f"No audio files found in '{self.input_directory}'.")
                return

            self.logger.info(f"Found {len(audio_files)} audio files to process.")

            for file_name in tqdm(audio_files, desc="Processing audio files"):
                self._process_single_file(file_name)

    def _process_single_file(self, file_name):
        """
        Process a single audio file: convert, transcribe, and save.

        Args:
            file_name (str): Name of the file to process.
        """
        input_path = os.path.join(self.input_directory, file_name)

        if not file_name.endswith(".wav"):
            wav_file = self.converter.convert_to_wav(input_path)
            if not wav_file:
                self.logger.warning(f"Skipping '{file_name}' due to conversion error.")
                return
        else:
            wav_file = input_path

        try:
            segments = self.transcriber.transcribe(wav_file)
            self.saver.save_transcription(segments, file_name)
            self.logger.info(f"Successfully processed and saved transcription for '{file_name}'.")
        except Exception as e:
            self.logger.error(f"Error processing file '{file_name}': {e}")
