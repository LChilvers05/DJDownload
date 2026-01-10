# DJDownload

A Python tool for splitting DJ mix recordings into individual tracks with proper metadata. This tool takes a single raw audio file containing a DJ set and an iTunes playlist XML file, then automatically splits the audio into separate track files with complete ID3 tags.

## Features

- **Automatic Track Splitting**: Splits a continuous DJ mix recording into individual tracks based on track durations from an iTunes playlist
- **Metadata Preservation**: Automatically adds ID3 tags to output files including:
  - Title
  - Artist
  - Album
  - Album Artist
  - Genre
  - Year
  - Track Number/Total Tracks
- **High-Quality Output**: Exports tracks in AIFF format for maximum audio quality

## Requirements

- Python 3.x
- pydub
- mutagen

## Installation

1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install pydub mutagen
   ```

## Usage

### 1. Prepare Your Input Files

#### Raw Audio File
- Place your DJ mix recording in the `audio/` directory
- **Format requirement**: The raw audio file must be in **WAV format**
- File should be named to match your playlist (e.g., `Ipizza.wav`)

#### Playlist XML File
- Export your iTunes playlist to XML format:
  1. Open iTunes
  2. Select the playlist you want to export
  3. Go to **File > Library > Export Playlist...**
  4. Choose **XML** as the file format
  5. Save the file to the `playlists/` directory

**Important**: The track order in your playlist must match the order of tracks in your audio recording, and the track durations in the playlist should be accurate.

### 2. Update Configuration

Edit [src/main.py](src/main.py) to specify your files:

```python
def main():
    create_track_files(
        playlist_file="playlists/YourPlaylist.xml",
        audio_file="audio/YourMix.wav",
        output_dir="output/"
    )
```

### 3. Run the Tool

```bash
python src/main.py
```

### 4. Get Your Tracks

The individual track files will be saved to the `output/` directory in **AIFF format** with complete metadata.
