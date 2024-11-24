from src.app.pipelines.audio_processing import AudioProcessorBase


class AudioSplitter(AudioProcessorBase):
    """
    Splits audio_processing files into smaller chunks.
    """

    def process(
        self, input_file: str, chunk_duration_ms: int, output_file_prefix: str
    ) -> List[str]:
        try:
            self.logger.info(f"Splitting audio_processing file: {input_file}")
            audio = self.load_audio(input_file)
            chunks = [
                audio[i : i + chunk_duration_ms]
                for i in range(0, len(audio), chunk_duration_ms)
            ]
            chunk_files = []
            for idx, chunk in enumerate(chunks):
                chunk_file = f"{output_file_prefix}_chunk{idx}.{self.format}"
                chunk_files.append(self.save_audio(chunk, chunk_file))
            self.logger.info(f"Split audio_processing into {len(chunk_files)} chunks.")
            return chunk_files
        except Exception as e:
            self.logger.error(
                f"Error splitting audio_processing file {input_file}: {e}"
            )
            raise
