import os
from pydub import AudioSegment
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceManager

# Initialize the logger and performance manager
log_manager = LoggerManager()
logger = log_manager.get_logger()
perf_manager = PerformanceManager()

class AudioConverter:
    def __init__(self, input_directory='/app/audio_files', output_directory='/app/processed_audio', format='wav'):
        """
        Initialize the AudioConverter with input and output directories and format.
        """
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.format = format
        os.makedirs(self.output_directory, exist_ok=True)
        logger.info(f"AudioConverter initialized with input: {self.input_directory}, output: {self.output_directory}, format: {self.format}")

    @perf_manager.track_performance
    def convert_audio_format(self, input_file, output_format=None):
        """
        Converts an downloaders file to the specified format.

        Args:
            input_file (str): Path to the input downloaders file.
            output_format (str, optional): Format to convert the downloaders file to. Defaults to class attribute 'format'.
        """
        output_format = output_format or self.format
        try:
            audio = AudioSegment.from_file(input_file)
            output_file = os.path.join(self.output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}.{output_format}")
            audio.export(output_file, format=output_format)
            logger.info(f"Converted {input_file} to {output_format} format.")
            return output_file
        except Exception as e:
            logger.error(f"Error converting {input_file}: {e}")
            return None

    def batch_convert_audio_files(self):
        """
        Batch processes all downloaders files in the input directory and converts them to the specified format.
        """
        audio_files = [f for f in os.listdir(self.input_directory) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        if not audio_files:
            logger.info("No downloaders files found for conversion.")
            return

        logger.info(f"Starting batch conversion of {len(audio_files)} downloaders files.")
        for audio_file in audio_files:
            input_path = os.path.join(self.input_directory, audio_file)
            self.convert_audio_format(input_path)
        logger.info("Batch conversion completed.")
