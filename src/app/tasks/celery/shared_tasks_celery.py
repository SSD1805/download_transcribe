# src/app/tasks/dask/transcription_task.py
from dask.distributed import Client

from app.pipelines.transcription.transcription_pipeline import TranscriptionPipeline

client = Client("localhost:8786")


def transcription_pipeline_task(input_file: str, output_dir: str):
    pipeline = TranscriptionPipeline(output_dir=output_dir)
    return pipeline.run(input_file)
