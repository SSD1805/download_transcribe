from src.app.pipelines.audio import AudioProcessorBase


class AudioConverter(AudioProcessorBase):
    """
    Converts audio files to a specified format.
    """

    def process(
        self, input_file: str, output_file: str, target_format: str = "wav"
    ) -> str:
        self.format = target_format
        try:
            self.logger.info(f"Converting {input_file} to {target_format}")
            audio = self.load_audio(input_file)
            converted_file = self.save_audio(audio, output_file)
            self.logger.info(f"Successfully converted {input_file} to {target_format}")
            return converted_file
        except Exception as e:
            self.logger.error(f"Error converting {input_file} to {target_format}: {e}")
            raise
