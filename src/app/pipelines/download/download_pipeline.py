# src/app/pipelines/download/download_pipeline.py
from dependency_injector.wiring import Provide, inject
from src.infrastructure.app.app_container import AppContainer


class DownloadPipeline:
    """
    Pipeline for managing downloads (video, channel, playlist, or batch).
    """

    @inject
    def __init__(
        self,
        download_manager=Provide[AppContainer.download_manager],
        logger=Provide[AppContainer.logger],
    ):
        self.download_manager = download_manager
        self.logger = logger

    def run(self, url: str, download_type: str = "video"):
        """
        Run the download pipeline based on the specified type.
        :param url: The URL to download.
        :param download_type: Type of download ('video', 'channel', 'playlist', 'batch').
        """
        self.logger.info(f"Starting {download_type} download for URL: {url}")

        try:
            if download_type == "video":
                self.download_manager.download_video(url)
            elif download_type == "channel":
                self.download_manager.download_channel(url)
            elif download_type == "playlist":
                self.download_manager.download_playlist(url)
            else:
                raise ValueError(f"Unknown download type: {download_type}")

            self.logger.info(f"{download_type.capitalize()} download completed for URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed {download_type} download for URL: {url}: {e}")
            raise
