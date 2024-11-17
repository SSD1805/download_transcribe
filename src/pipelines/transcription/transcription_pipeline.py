# src/pipelines/transcription/transcription_pipeline.py
import os
from src.core.services import CoreServices
from src.pipelines.audio.audio_converter import AudioConverter
from src.pipelines.transcription.audio_transcriber import AudioTranscriber
from src.pipelines.transcription.transcription_saver import TranscriptionSaver

class TranscriptionPipeline:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.logger = CoreServices.get_logger()
        self.perf_tracker = CoreServices.get_performance_tracker()
        self.converter = AudioConverter(output_directory=output_directory)
        self.transcriber = AudioTranscriber()
        self.saver = TranscriptionSaver(output_directory=output_directory)

    def process_files(self):
        """
        Process all audio files in the input directory.
        """
        self.logger.info(f"Starting transcription pipeline for {self.input_directory}")
        audio_files = [
            f for f in os.listdir(self.input_directory) if f.endswith(('.mp3', '.wav', '.flac'))
        ]
        for file_name in audio_files:
            input_path = os.path.join(self.input_directory, file_name)
            self._process_file(input_path)

    def _process_file(self, input_file):
        """
        Process a single audio file: convert, transcribe, and save.
        """
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
