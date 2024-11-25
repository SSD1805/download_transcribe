# src/app/tasks/celery/audio_processing_task.py
from celery import Celery

from src.app.pipelines.transcription.audio_processing_pipeline import (
    AudioProcessingPipeline,
)
from src.app.tasks.base_task import BaseTask
from src.app.tasks.observers.logger_observer import LoggerObserver

app = Celery("tasks", broker="redis://localhost:6379/0")

class AudioProcessingTask(BaseTask):
    def process(self, input_file, output_dir):
        pipeline = AudioProcessingPipeline(output_dir=output_dir)
        return pipeline.run(input_file)

@app.task
def audio_processing_pipeline_task(input_file: str, output_dir: str):
    task = AudioProcessingTask()
    task.add_observer(LoggerObserver(task.logger))
    return task.execute(task.process, input_file, output_dir)
