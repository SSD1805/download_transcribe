# YouTube Audio Downloader and Transcriber

This project provides a comprehensive tool to download audio from YouTube videos or channels using `yt-dlp`, transcribe the audio using Whisper AI, and process the transcriptions for further analysis. It incorporates robust error handling, modular structure, and clear configuration options to enhance functionality and maintainability.

## Features
### Audio and Transcription
- **Audio Download**: Utilizes `yt-dlp` to download audio from YouTube in `.mp3` format, supporting both individual videos and entire channels.
- **Transcription**: Automatically transcribes audio files using WhisperX and saves the transcriptions as `.txt` files.
- **Skip Existing Files**: Checks if both the audio file and its transcription already exist, skipping redundant processes.

### Modular Structure and Processing
- **Modular Codebase**: Separate modules for audio processing, file management, transcription, configuration management, and text processing.
- **Processing Transcriptions**: Segments transcriptions into sentences, applies NER using spaCy, and tokenizes sentences with NLTK.
- **Folder Management**: Organizes audio files in `/app/audio_files` and transcriptions in `/app/transcriptions`.
- **File Management**: Manages file paths, sanitizes file names, tracks progress, and logs metadata to CSV.

### Configuration and Logging
- **Configuration**: Customizable settings in `config.yaml` for download delay, Whisper model size, directories, etc.
- **Logging**: Configurable logging through `logger.py`, supporting both console and file logging based on `.env` settings.
- **Environment Variable Support**: Uses `python-dotenv` to load environment variables from a `.env` file.

### Deployment and Containerization
- **Docker Support**: Contains a `Dockerfile` for building a consistent deployment image.
- **Environment Variables**: Easily configured through a `.env` file.

## Project Structure
```
/app
|-- audio_files
|-- logs
|-- podcast_audio
|-- transcriptions
|-- src
    |-- modules
        |-- audio_processing.py
        |-- config_manager.py
        |-- file_manager.py
        |-- logger.py
        |-- text_processor.py
        |-- transcriber.py
        |-- transcription_manager.py
        |-- youtube_downloader.py
    |-- scripts
    |-- utils
        |-- helper_functions.py
|-- tests
.env
app.py
config.yaml
Dockerfile
pyproject.toml
README.md
```

## Requirements
- **Python**: Ensure Python 3.12 or higher is installed.
- **yt-dlp**: Tool for downloading YouTube audio.
- **WhisperX**: Advanced ASR tool with word-level timestamps and alignment.
- **ffmpeg**: Essential for audio extraction and conversion.
- **Additional Libraries**:
  - `torch`: Core dependency for machine learning tasks.
  - `speechbrain`: For advanced audio processing.
  - `numpy`, `pandas`, `scipy`: For data manipulation and scientific computing.
  - `nltk`, `spacy`, `spacy-transformers`: For NLP tasks.
  - `pydub`, `soundfile`: Audio manipulation and file handling.
  - `requests`, `tqdm`, `tenacity`, `python-dotenv`, `pyyaml`: Various utility functions and environment handling.

## Installation

### 1. Clone the Repository
Clone this repository to your local machine.

### 2. Install Dependencies Using Poetry
Ensure `Poetry` is installed. Run the following command:

```bash
poetry install
```

This command reads `pyproject.toml` and `poetry.lock` to set up the environment with all necessary dependencies.

### 3. Install ffmpeg
Install `ffmpeg` by following the instructions based on your operating system. This step is essential for `yt-dlp` to extract and convert audio files.

## Usage

### Run the Application

```bash
poetry run python app.py
```

### Command-line Arguments
The `app.py` file supports various command-line arguments for running different modules:

```bash
poetry run python app.py download --url "https://youtube.com/your-video"
poetry run python app.py transcribe modules.mp3 --title "Your Title"
poetry run python app.py process --directory "/app/transcriptions"
poetry run python app.py setup --config-path "config.yaml"
poetry run python app.py manage_files --directory "/app/audio_files"
```

### Using Click
The application uses the `click` library to create a command-line interface (CLI). Here are the available commands:

- **download**: Downloads audio from a YouTube URL.
  ```bash
  poetry run python app.py download --url "https://youtube.com/your-video"
  ```

- **transcribe**: Transcribes the provided audio file.
  ```bash
  poetry run python app.py transcribe modules.mp3 --title "Your Title"
  ```

- **process**: Processes transcriptions for NER and sentence segmentation.
  ```bash
  poetry run python app.py process --directory "/app/transcriptions"
  ```

- **setup**: Sets up configuration for the application.
  ```bash
  poetry run python app.py setup --config-path "config.yaml"
  ```

- **manage_files**: Manages files in the specified directory.
  ```bash
  poetry run python app.py manage_files --directory "/app/audio_files"
  ```

### Example Workflows

#### Scenario 1: Processing Pre-existing Audio Files
If you already have audio files and want to transcribe and process them, you can use the `transcribe` and `process` commands.

1. **Transcribe an Audio File**:
   ```bash
   poetry run python app.py transcribe /path/to/modules.mp3 --title "Existing Audio"
   ```

2. **Process Transcriptions**:
   ```bash
   poetry run python app.py process --directory "/app/transcriptions"
   ```

#### Scenario 2: Downloading and Processing Audio Files
If you want to download audio files from YouTube and then process them through the rest of the modules, you can chain the commands.

1. **Download Audio from YouTube**:
   ```bash
   poetry run python app.py download --url "https://youtube.com/your-video"
   ```

2. **Transcribe the Downloaded Audio**:
   ```bash
   poetry run python app.py transcribe /app/audio_files/downloaded_audio.mp3 --title "Downloaded Audio"
   ```

3. **Process Transcriptions**:
   ```bash
   poetry run python app.py process --directory "/app/transcriptions"
   ```

#### Scenario 3: Full Workflow Automation
To automate the entire workflow from downloading to processing, you can create a script that runs all the commands sequentially.

```bash
#!/bin/bash

# Download modules from YouTube
poetry run python app.py download --url "https://youtube.com/your-video"

# Transcribe the downloaded modules
poetry run python app.py transcribe /app/audio_files/downloaded_audio.mp3 --title "Downloaded Audio"

# Process the transcriptions
poetry run python app.py process --directory "/app/transcriptions"
```

Save this script as `run_workflow.sh` and execute it:
```bash
bash run_workflow.sh
```

## Configuration
Configure the `config.yaml` file for customizable settings like download delay, directories, Whisper model size, and more.

## Logging
The project uses `logger.py` to handle logging, configured via environment variables set in the `.env` file:

```
LOG_FILE_PATH=/app/logs/app.log
LOG_LEVEL=10
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
ENABLE_CONSOLE_LOGGING=true
ENABLE_FILE_LOGGING=true
```

## Testing
The `tests` folder contains unit tests for individual modules to ensure that components like `audio_processing`, `file_manager`, and `transcriber` work as expected. Use the following command to run tests:

```bash
pytest tests/
```

## License
This project is licensed under the MIT License.
