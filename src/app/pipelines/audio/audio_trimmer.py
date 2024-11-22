from src.app.pipelines.audio import AudioProcessorBase


class AudioTrimmer(AudioProcessorBase):
    """
    Trims silence from the beginning and end of audio files.
    """

    def process(
        self, input_file: str, output_file: str, silence_thresh: int = -40
    ) -> str:
        try:
            self.logger.info(f"Trimming silence from {input_file}")
            audio = self.load_audio(input_file)
            trimmed_audio = audio.strip_silence(silence_thresh=silence_thresh)
            trimmed_file = self.save_audio(trimmed_audio, output_file)
            self.logger.info(f"Successfully trimmed {input_file}")
            return trimmed_file
        except Exception as e:
            self.logger.error(f"Error trimming audio file {input_file}: {e}")
            raise
