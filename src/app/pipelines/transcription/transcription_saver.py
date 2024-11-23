import json
import os

from src.app.pipelines.transcription.basepipeline import BasePipeline


class TranscriptionSaver(BasePipeline):
    """
    Handles saving transcription results in various formats.
    """

    def __init__(self, output_directory: str):
        super().__init__()
        self.output_directory = output_directory
        self.ensure_directory_exists(self.output_directory)

    def save_transcription(self, segments, file_name: str, format="txt"):
        """
        Saves transcription data to the specified file format.
        """
        output_file = os.path.join(self.output_directory, f"{file_name}.{format}")

        with self.track(f"Saving transcription for {file_name}"):
            if format == "txt":
                self._save_as_txt(segments, output_file)
            elif format == "json":
                self._save_as_json(segments, output_file)
            else:
                self.logger.error(f"Unsupported format: {format}")

    def _save_as_txt(self, segments, output_file):
        """
        Saves transcription as a plain text file.
        """
        with open(output_file, "w") as f:
            for segment in segments:
                f.write(f"{segment['text']}\n")
        self.logger.info(f"Saved transcription to {output_file} (txt)")

    def _save_as_json(self, segments, output_file):
        """
        Saves transcription as a JSON file.
        """
        with open(output_file, "w") as f:
            json.dump(segments, f, indent=4)
        self.logger.info(f"Saved transcription to {output_file} (json)")
