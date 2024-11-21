# This module is responsible for saving the transcriptions to a file.
import os
import json
from src.utils.structlog_logger import StructLogger
from src.utils.tracking_utilities import PerformanceTracker

class TranscriptionSaver:
    def __init__(self, output_directory):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)
        self.logger = StructLogger.get_logger()
        self.performance_tracker = PerformanceTracker.get_instance()

    def save_transcription(self, segments, audio_file, format='txt'):
        output_file = os.path.join(
            self.output_directory, f"{os.path.splitext(os.path.basename(audio_file))[0]}.{format}"
        )
        try:
            with self.performance_tracker.track_execution("Save Transcription"):
                if format == 'txt':
                    self._save_as_txt(segments, output_file)
                elif format == 'json':
                    self._save_as_json(segments, output_file)
                else:
                    raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            self.logger.error(f"Error saving transcription for {audio_file}: {e}")

    def _save_as_txt(self, segments, output_file):
        with open(output_file, 'w') as f:
            for segment in segments:
                f.write(f"{segment['text']}\n")
        self.logger.info(f"Transcription saved to {output_file} (txt)")

    def _save_as_json(self, segments, output_file):
        with open(output_file, 'w') as f:
            json.dump(segments, f, indent=4)
        self.logger.info(f"Transcription saved to {output_file} (json)")
