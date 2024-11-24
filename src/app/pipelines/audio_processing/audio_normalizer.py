from pydub import effects

from src.app.pipelines.audio_processing import AudioProcessorBase


class AudioNormalizer(AudioProcessorBase):
    """
    Normalizes audio_processing files to a standard volume level.
    """

    def process(self, input_file: str, output_file: str) -> str:
        try:
            self.logger.info(f"Normalizing audio_processing file: {input_file}")
            audio = self.load_audio(input_file)
            normalized_audio = effects.normalize(audio)
            normalized_file = self.save_audio(normalized_audio, output_file)
            self.logger.info(f"Successfully normalized {input_file}")
            return normalized_file
        except Exception as e:
            self.logger.error(
                f"Error normalizing audio_processing file {input_file}: {e}"
            )
            raise
