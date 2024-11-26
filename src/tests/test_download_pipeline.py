import pytest
from unittest.mock import MagicMock
from src.app.pipelines.download.download_pipeline import DownloadPipeline

@pytest.fixture
def download_manager():
    return MagicMock()

@pytest.fixture
def logger():
    return MagicMock()


@pytest.fixture
def download_pipeline(download_manager, logger):
    return DownloadPipeline(download_manager=download_manager, logger=logger)

def test_run_video_download(download_pipeline, download_manager, logger):
    url = "http://example.com/video"
    download_pipeline.run(url, "video")
    download_manager.download_video.assert_called_once_with(url)
    logger.info.assert_any_call(f"Starting video download for URL: {url}")
    logger.info.assert_any_call(f"Video download completed for URL: {url}")

def test_run_unknown_download_type(download_pipeline, logger):
    url = "http://example.com/unknown"
    with pytest.raises(ValueError, match="Unknown download type: unknown"):
        download_pipeline.run(url, "unknown")
    logger.error.assert_called_once()