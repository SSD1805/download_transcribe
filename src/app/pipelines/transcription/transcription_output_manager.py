from src.pipelines.base_pipeline import BasePipeline


class TranscriptionSaver(BasePipeline):
    """
    Handles saving transcription results.
    """

    def __init__(self, output_directory: str):
        super().__init__()
        self.output_directory = output_directory
        self.ensure_directory_exists(self.output_directory)

    def save_transcription(self, segments, audio_file: str, format="txt"):
        output_file = f"{self.output_directory}/{audio_file}.{format}"
        with self.track("Save Transcription"):
            if format == "txt":
                self._save_as_txt(segments, output_file)
            elif format == "json":
                self._save_as_json(segments, output_file)
            else:
                self.logger.error(f"Unsupported format: {format}")

    def _save_as_txt(self, segments, output_file):
        with open(output_file, "w") as f:
            for segment in segments:
                f.write(f"{segment['text']}\n")
        self.logger.info(f"Saved transcription to {output_file} (txt)")

    def _save_as_json(self, segments, output_file):
        import json
        with open(output_file, "w") as f:
            json.dump(segments, f, indent=4)
        self.logger.info(f"Saved transcription to {output_file} (json)")
