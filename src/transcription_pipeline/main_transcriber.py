import os
from tqdm import tqdm
from audio_converter import AudioConverter
from audio_transcriber import AudioTranscriber
from transcription_saver import TranscriptionSaver
from src.core.performance_tracker import PerformanceManager

perf_manager = PerformanceManager()


@perf_manager.track_performance
def process_audio_files(input_directory='/app/audio_files'):
    converter = AudioConverter()
    transcriber = AudioTranscriber()
    saver = TranscriptionSaver()

    audio_files = [f for f in os.listdir(input_directory) if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]

    for file_name in tqdm(audio_files, desc="Processing audio_pipeline files"):
        input_path = os.path.join(input_directory, file_name)
        wav_file = converter.convert_to_wav(input_path) if not file_name.endswith('.wav') else input_path

        if not wav_file:
            logger.warning(f"Skipping '{file_name}' due to conversion error.")
            continue

        segments = transcriber.transcribe(wav_file)
        saver.save_transcription(segments, file_name)


if __name__ == "__main__":
    perf_manager.monitor_memory_usage()  # Start monitoring memory usage if needed
    process_audio_files()
