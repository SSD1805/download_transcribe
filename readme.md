
---

# YouTube Audio Downloader and Transcriber with Whisper AI

This project downloads audio from YouTube videos and transcribes them using Whisper AI. 

I tried to design this repo with ease of use in mind. I'm hoping it's accessible to non-technical users exploring how to code as well as beginner coders.


## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Module Breakdown](#module-breakdown)
- [Common Issues](#common-issues)
- [Next Steps and Customization](#next-steps-and-customization)

## Overview

This project automates the process of:
1. **Downloading audio from YouTube** using `yt-dlp`.
2. **Transcribing audio files** into text using Whisper AI.
3. **Organizing files** using a dedicated file management module.

## Project Structure

```
.
├── main.py              # Central script to run the project
├── audio_downloader.py  # Downloads audio from YouTube
├── transcriber.py       # Transcribes audio files
├── file_manager.py      # Manages files and directories
├── podcast_audio        # Stores downloaded audio files
├── transcriptions       # Stores transcriptions
└── README.md            # Documentation
```

- **`main.py`**: Orchestrates downloading and transcribing.
- **`audio_downloader.py`**: Handles audio downloads.
- **`transcriber.py`**: Transcribes audio using Whisper AI.
- **`file_manager.py`**: Ensures proper file organization.

## Installation

### Prerequisites

- **Python 3.9+**
- **`ffmpeg`**: Required for `yt-dlp` to handle audio extraction.
- **Environment Variables** (Optional):
  - `FFMPEG_PATH`: Path to `ffmpeg` executable.
  - `WHISPER_MODEL_SIZE`: Specify the Whisper model size (`"base"`, `"small"`, etc.).
  - `TRANSCRIPTION_FORMAT`: Format for transcriptions (`"txt"` or `"json"`).

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Install Required Packages**:
   Run this command to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Requirements

- **Python**: Ensure you have Python 3.x installed.
- **yt-dlp**: A powerful tool to download videos and audio from YouTube.
- **Whisper AI**: An automatic speech recognition (ASR) system for transcription.
- **ffmpeg**: A command-line tool used by `yt-dlp` to extract and convert audio formats.

## Installation

### 1. Clone the Repository
Download or clone this repository to your local machine.

### 2. Install Python Packages

Run the following command to install the required Python packages:

```bash
pip install yt-dlp whisper
```

### 3. Install `ffmpeg`

`ffmpeg` is required for `yt-dlp` to extract and convert audio files. Follow the instructions below based on your operating system.

#### **Windows**:

1. Download `ffmpeg` from the official site: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
   - Download the **Windows build**.
   
2. Extract the downloaded `.zip` file and move the extracted folder (e.g., `ffmpeg-<version>-full_build`) to a desired location (e.g., `C:\ffmpeg`).

3. Add `ffmpeg` to your system's `PATH`:
   - Open **Control Panel** → **System and Security** → **System** → **Advanced system settings**.
   - Click on **Environment Variables**.
   - In the **System variables** section, find the `Path` variable and click **Edit**.
   - Click **New** and add the path to the `bin` directory of `ffmpeg` (e.g., `C:\ffmpeg\bin`).
   - Click **OK** to close all windows.

4. Verify the installation by opening the command prompt and typing:

```bash
ffmpeg -version
```

You should see the version information for `ffmpeg`.

#### **Linux (Ubuntu/Debian)**:

Run the following commands to install `ffmpeg`:

```bash
sudo apt update
sudo apt install ffmpeg
```

Verify the installation by running:

```bash
ffmpeg -version
```

#### **macOS**:

If you have **Homebrew** installed, you can use it to install `ffmpeg`:

```bash
brew install ffmpeg
```

Verify the installation by running:

```bash
ffmpeg -version
```

### 4. Install Additional Dependencies for Whisper

You may also need to install additional dependencies for Whisper, such as `torch`:

```bash
pip install torch
```



4. **Set Up Environment Variables** (Optional):
   These can improve functionality if set up.
   - **Linux/macOS**:
     ```bash
     export FFMPEG_PATH="/path/to/ffmpeg"
     export WHISPER_MODEL_SIZE="base"
     export TRANSCRIPTION_FORMAT="txt"
     ```
   - **Windows**:
     ```cmd
     set FFMPEG_PATH=C:\path\to\ffmpeg
     set WHISPER_MODEL_SIZE=base
     set TRANSCRIPTION_FORMAT=txt
     ```

5. **Run in Docker (Optional)**:
   To run the project in a containerized environment:
   ```bash
   docker build -t your_image_name .
   docker run -v $(pwd)/podcast_audio:/app/podcast_audio -v $(pwd)/transcriptions:/app/transcriptions your_image_name
   ```

## How to Run

1. **Set the YouTube Channel URL in `main.py`**:
   Update the `channel_url` variable in `main.py` with the YouTube channel or playlist URL.

2. **Run the Main Script**:
   ```bash
   python main.py
   ```

   The script will automatically download and transcribe videos from the specified YouTube channel.

## Module Breakdown

### 1. `audio_downloader.py`

Handles downloading audio from YouTube.

- **Features**:
  - **Progress Logging**: Provides download progress updates.
  - **Retry Mechanism**: Retries downloads on network failure.
  - **Dynamic `ffmpeg` Path**: Reads the `ffmpeg` location from `FFMPEG_PATH`.

- **Code Sample**:
  ```python
  import yt_dlp

  ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
      'outtmpl': './podcast_audio/%(title)s.%(ext)s',
      'ignoreerrors': True,
  }

  def download_audio(video_url):
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download([video_url])
  ```

### 2. `transcriber.py`

Uses Whisper AI to transcribe audio files to text.

- **Configurable Model**: Select Whisper model size with `WHISPER_MODEL_SIZE`.
- **Flexible Output Formats**: Transcriptions can be saved as `.txt` or `.json`.

- **Code Sample**:
  ```python
  import whisper

  whisper_model = whisper.load_model("base")

  def transcribe_audio(audio_file, title, transcriptions_dir):
      result = whisper_model.transcribe(audio_file)
      with open(f"{transcriptions_dir}/{title}.txt", 'w') as f:
          f.write(result['text'])
  ```

### 3. `file_manager.py`

Utility functions to manage files and directories.

- **Ensures Directories Exist**: Verifies required folders are created.
- **File Existence Check**: Skips existing files to avoid reprocessing.

- **Code Sample**:
  ```python
  import os

  def ensure_directories_exist(*directories):
      for directory in directories:
          if not os.path.exists(directory):
              os.makedirs(directory)

  def sanitize_filename(title):
      return ''.join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in title)
  ```

### 4. `main.py`

Orchestrates the downloading and transcribing.

- **Parallel Processing**: Allows concurrent downloads and transcriptions using `ThreadPoolExecutor`.
- **Usage of `max_workers`**:
  - **Why**: Parallel processing speeds up large playlists.
  - **Adjustable**: `max_workers` can be increased or decreased based on system capacity.

- **Code Sample**:
  ```python
  from audio_downloader import download_audio_from_channel
  from transcriber import transcribe_audio
  from file_manager import ensure_directories_exist, files_exist

  def download_and_transcribe(channel_url):
      video_entries = download_audio_from_channel(channel_url)
      for video_info in video_entries:
          if not files_exist(video_info['title']):
              download_audio(video_info['url'])
              transcribe_audio(video_info['title'])
  ```

## Common Issues

1. **`ffmpeg` Not Found**:
   - Ensure `ffmpeg` is installed and added to the system `PATH`.

2. **Unavailable Videos**:
   - Some videos might be private or restricted. The script skips such videos and logs the error.

3. **Slow Transcription**:
   - Whisper AI can be slow for long files. To speed up, try smaller models by adjusting `WHISPER_MODEL_SIZE`.

4. **Large File Sizes**:
   - Ensure enough storage for downloaded audio files, especially for long playlists.

## Next Steps and Customization

### Ideas for Expansion

1. **Advanced Whisper Models**:
   - Experiment with larger Whisper models for improved transcription accuracy.

2. **Batch Processing**:
   - Automate the script to run at scheduled intervals.

3. **Support for Multiple Platforms**:
   - Extend the `audio_downloader` module to download from other platforms like Vimeo.

4. **Enhanced File Management**:
   - Use a database to manage and track processed files, particularly useful for large datasets.

## License

This project is licensed under the MIT License.

--- 

