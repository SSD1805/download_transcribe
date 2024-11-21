# Description: This file defines the AudioProcessingPipeline class which is responsible for processing audio files
import os
from tqdm import tqdm
from src.app.pipelines.audio.audio_converter import AudioConverter
from src.app.pipelines.transcription.audio_transcriber import AudioTranscriber
from src.app.pipelines.transcription.transcription_saver import TranscriptionSaver
from src.app.utils.structlog_logger import StructLogger
from src.app.utils.tracking_utilities import PerformanceTracker


class AudioProcessingPipeline:
    def __init__(
        self,
        input_directory,
        output_directory,
        converter=None,
        transcriber=None,
        saver=None,
    ):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.logger = StructLogger.get_logger()
        self.perf_tracker = PerformanceTracker.get_instance()

        self.converter = converter or AudioConverter(output_directory=output_directory)
        self.transcriber = transcriber or AudioTranscriber()
        self.saver = saver or TranscriptionSaver(output_directory=output_directory)

    def process_files(self):
        with self.perf_tracker.track_execution("Audio Processing Pipeline"):
            if not os.path.exists(self.input_directory):
                self.logger.error(
                    f"Input directory '{self.input_directory}' does not exist."
                )
                return

            audio_files = [
                f
                for f in os.listdir(self.input_directory)
                if f.endswith((".mp3", ".wav", ".m4a", ".flac"))
            ]

            if not audio_files:
                self.logger.warning(
                    f"No audio_processor files found in '{self.input_directory}'."
                )
                return

            self.logger.info(
                f"Found {len(audio_files)} audio_processor files to process."
            )

            for file_name in tqdm(audio_files, desc="Processing audio_processor files"):
                self._process_single_file(file_name)

    def _process_single_file(self, file_name):
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
            self.logger.info(
                f"Successfully processed and saved transcription for '{file_name}'."
            )
        except Exception as e:
            self.logger.error(f"Error processing file '{file_name}': {e}")
