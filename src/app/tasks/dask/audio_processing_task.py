# src/app/tasks/dask/audio_processing_task.py
from dask.distributed import Client
from app.pipelines.audio.audio_pipeline import AudioProcessingPipeline

client = Client("localhost:8786")

def process_audio_pipeline(input_file: str, output_dir: str):
    pipeline = AudioProcessingPipeline(output_dir=output_dir)
    return pipeline.run(input_file)
