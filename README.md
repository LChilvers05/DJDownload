# DJDownload

Takes an iTunes/Music playlist export (`.xml`) plus a matching continuous recording (`.wav`), slices the audio on silence, and exports individual tracks as `.aiff` files with ID3 metadata.

## Requirements

- Python 3
- `ffmpeg` available on your `PATH`
  - macOS (Homebrew): `brew install ffmpeg`

## Project layout

- `playlists/*.xml`: exported iTunes/Music playlists
- `audio/<playlist_name>.wav`: one WAV recording per playlist
- `output/<playlist_name>/*.aiff`: exported tracks
- `temp/*.wav`: intermediate slices (recreated each run)

The playlist name is taken from the XML filename (e.g. `playlists/Ipizza.xml` → `Ipizza`), and the code expects the audio to be at `audio/Ipizza.wav`.

## Setup

```bash
make setup
```

## Run

```bash
make run
```

The default Make target is `run`, so `make` also works once you’ve run `make setup`.

## Exporting playlists

See [playlists/README.md](playlists/README.md) for the iTunes/Music “Export Playlist…” steps.

## How it works (high level)

1. For each `playlists/*.xml`, parse the playlist and track metadata.
2. Slice `audio/<playlist>.wav` into `temp/temp_000.wav`, `temp/temp_001.wav`, …
   - Uses `ffmpeg` `silencedetect` to find `silence_end` timestamps.
   - Uses the `ffmpeg` segment muxer to split at those timestamps.
3. Load each slice and match it to the next expected playlist track by duration (with a small tolerance).
4. Export as `.aiff` into `output/<playlist_name>/` and write tags (title/artist/album/etc).

## Tuning / troubleshooting

- If slicing produces too many/few segments, adjust the silence detection parameters in [src/audio_processor.py](src/audio_processor.py) (`threshold`/`duration`).
- If tracks don’t match, adjust the duration tolerance in [src/main.py](src/main.py).
- If `ffmpeg` isn’t found, confirm `ffmpeg -version` works in your shell.

## Useful commands

- `make clean`: removes `venv/` and Python cache files
