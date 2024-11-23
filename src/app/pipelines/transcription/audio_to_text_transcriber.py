from src.app.pipelines.transcription.basepipeline import BasePipeline


class AudioTranscriber(BasePipeline):
    """
    Handles audio-to-text transcription.
    """

    def __init__(self, transcription_service):
        super().__init__()
        self.transcription_service = transcription_service

    def transcribe(self, audio_file: str):
        """
        Transcribes an audio file into text segments.
        """
        with self.track("Audio Transcription"):
            self.logger.info(f"Transcribing file: {audio_file}")
            return self.transcription_service.transcribe(audio_file)
