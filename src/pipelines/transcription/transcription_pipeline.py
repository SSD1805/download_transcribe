# Description: This file defines the transcription pipeline class which is responsible for processing audio files in a given directory.
import os
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

class TranscriptionPipeline:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.logger = StructLogger.get_logger()
        self.perf_tracker = PerformanceTracker.get_instance()

    def process_files(self):
        self.logger.info(f"Starting transcription pipeline for {self.input_directory}")
        audio_files = [
            f for f in os.listdir(self.input_directory) if f.endswith(('.mp3', '.wav', '.flac'))
        ]
        for file_name in audio_files:
            input_path = os.path.join(self.input_directory, file_name)
            self._process_file(input_path)

    def _process_file(self, input_file):
        with self.perf_tracker.track_execution(f"Processing {input_file}"):
            # Convert if necessary
            wav_file = self.converter.convert_to_wav(input_file)
            if not wav_file:
                self.logger.error(f"Skipping {input_file} due to conversion failure.")
                return

            # Transcribe
            segments = self.transcriber.transcribe(wav_file)
            if not segments:
                self.logger.error(f"Skipping {input_file} due to transcription failure.")
                return

            # Save transcription
            self.saver.save_transcription(segments, wav_file)
            self.logger.info(f"Successfully processed {input_file}")
