import os
from unittest.mock import patch
from pydub import AudioSegment
from src.pipelines.audio.audio_converter import AudioConverter

# Fixture for the AudioConverter
@pytest.fixture
def audio_converter(tmp_path):
    """
    Fixture to provide an AudioConverter instance with temporary directories.
    """
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return AudioConverter(input_directory=str(input_dir), output_directory=str(output_dir))

# Test Invalid Input Directory
def test_invalid_input_directory(tmp_path):
    """
    Test behavior when the input directory does not exist.
    """
    invalid_input_dir = str(tmp_path / "non_existent_input")
    with pytest.raises(FileNotFoundError):
        AudioConverter(input_directory=invalid_input_dir)

# Test Empty Audio File
@patch("src.audio.audio_converter.AudioSegment.from_file")
def test_empty_audio_file(mock_from_file, audio_converter, tmp_path):
    """
    Test conversion of an empty audio file.
    """
    mock_from_file.side_effect = Exception("Empty file or unsupported format")
    empty_file = tmp_path / "input" / "empty.mp3"
    empty_file.touch()  # Create an empty file

    result = audio_converter.convert_audio_format(str(empty_file))

    mock_from_file.assert_called_once_with(str(empty_file))
    assert result is None

# Test Unsupported File Format
def test_unsupported_file_format(audio_converter, tmp_path):
    """
    Test behavior when encountering unsupported file extensions.
    """
    unsupported_file = tmp_path / "input" / "unsupported_file.xyz"
    unsupported_file.touch()  # Create a dummy unsupported file

    result = audio_converter.convert_audio_format(str(unsupported_file))
    assert result is None

# Test Read-Only Output Directory
@patch("src.audio.audio_converter.AudioSegment.from_file")
@patch("src.audio.audio_converter.AudioSegment.export")
def test_read_only_output_directory(mock_export, mock_from_file, audio_converter, tmp_path):
    """
    Test behavior when the output directory is read-only.
    """
    read_only_dir = tmp_path / "output"
    os.chmod(read_only_dir, 0o444)  # Make the directory read-only
    mock_from_file.return_value = AudioSegment()

    input_file = tmp_path / "input" / "test.mp3"
    input_file.write_text("dummy audio data")

    result = audio_converter.convert_audio_format(str(input_file))

    assert result is None
    mock_from_file.assert_called_once_with(str(input_file))

# Test Special Characters in Filenames
@patch("src.audio.audio_converter.AudioSegment.from_file")
@patch("src.audio.audio_converter.AudioSegment.export")
def test_special_characters_in_filenames(mock_export, mock_from_file, audio_converter, tmp_path):
    """
    Test filenames with special characters.
    """
    mock_from_file.return_value = AudioSegment()

    special_file = tmp_path / "input" / "spéci@l#file$.mp3"
    special_file.write_text("dummy audio data")

    result = audio_converter.convert_audio_format(str(special_file))

    mock_from_file.assert_called_once_with(str(special_file))
    assert result.endswith("spéci@l#file$.wav")

# Test Large Audio File
@patch("src.audio.audio_converter.AudioSegment.from_file")
@patch("src.audio.audio_converter.AudioSegment.export")
def test_large_audio_file(mock_export, mock_from_file, audio_converter, tmp_path):
    """
    Test conversion of a very large audio file.
    """
    mock_from_file.return_value = AudioSegment()

    large_file = tmp_path / "input" / "large_file.mp3"
    with open(large_file, "wb") as f:
        f.write(b"\0" * 1024 * 1024 * 1024)  # Simulate a 1GB file

    result = audio_converter.convert_audio_format(str(large_file))

    mock_from_file.assert_called_once_with(str(large_file))
    assert result.endswith("large_file.wav")
