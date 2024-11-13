from src.audio_pipeline.audio_converter import AudioConverter
from src.audio_pipeline.audio_splitter import AudioSplitter
from src.audio_pipeline.audio_normalizer import AudioNormalizer
from src.audio_pipeline.audio_trimmer import AudioTrimmer
from src.audio_pipeline.cli_audio import AudioCLI

class AudioHandler:
    def __init__(self, input_directory='/app/audio_files', output_directory='/app/processed_audio', format='wav'):
        self.audio_converter = AudioConverter(output_directory, format)
        self.audio_splitter = AudioSplitter(output_directory, format)
        self.audio_normalizer = AudioNormalizer(output_directory, format)
        self.audio_trimmer = AudioTrimmer(output_directory, format)
        self.audio_cli = AudioCLI(input_directory, output_directory, format)

    def convert(self, input_file, output_format=None):
        return self.audio_converter.convert(input_file, output_format)

    def split(self, input_file, segment_duration=30000):
        return self.audio_splitter.split(input_file, segment_duration)

    def normalize(self, input_file):
        return self.audio_normalizer.normalize(input_file)

    def trim(self, input_file):
        return self.audio_trimmer.trim(input_file)

    def run_cli(self):
        self.audio_cli.run()
