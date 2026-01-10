# DJDownload

Split a single long DJ mix/recording into individual track files using an exported Apple Music/iTunes playlist (XML).

This tool:
- Reads track order + durations from a playlist XML
- Slices a matching `audio/<playlist>.wav` into per-track files
- Exports each track as `.aiff` and writes common tags (title/artist/album/etc.)

## Prerequisites

- macOS (this repo layout assumes macOS, but it should work elsewhere)
- Python 3
- `make`
- (Recommended) `ffmpeg` for `pydub`

On macOS:

```bash
brew install ffmpeg
```

## Setup

```bash
make setup
```

This creates `./venv` and installs dependencies (`pydub`, `mutagen`).

## Usage

1) Export a playlist XML into `playlists/`

- In Music/iTunes: **File → Library → Export Playlist…**
- Choose **XML**
- Save it into `playlists/` (example: `playlists/Fresh Chiz.xml`)

Important: the playlist name *inside the XML* must match the filename (without `.xml`).

2) Put the matching audio recording into `audio/`

For `playlists/Fresh Chiz.xml`, you must have:

- `audio/Fresh Chiz.wav`

The WAV should be the full continuous recording that corresponds to that playlist *in the same order*, starting at time 0.

3) Run

```bash
make run
```

The script processes every `*.xml` in `playlists/`.

## Output

For each playlist XML, tracks are written to:

- `output/<playlist name>/`

Each track is exported as:

- `output/<playlist name>/<Track Title>.aiff`

Tags written (when present in the playlist XML):
- Title, Artist
- Album, Album Artist
- Genre, Year
- Track number / track count

## How slicing works (important)

Slicing is sequential using durations from the XML (the `Total Time` field, in milliseconds):

- Track 1: starts at 0
- Track 2: starts after Track 1 duration
- …and so on

There is no beat detection, silence detection, or cue-point logic. If your recording does not align with the playlist durations/order, the cuts will drift.

## Troubleshooting

- **"Virtual environment not found"**: run `make setup` first.
- **Audio file not found**: ensure `audio/<playlist>.wav` exists and the name matches the XML filename.
- **"Playlist '<name>' not found in file"**: the playlist name embedded in the XML doesn’t match the XML filename (without `.xml`).
- **ffmpeg errors / decoding issues**: ensure `ffmpeg` is installed (`brew install ffmpeg`).

## Project layout

- `src/` — application code
- `playlists/` — exported playlist XML files
- `audio/` — input WAV recordings (one per playlist)
- `output/` — generated AIFF tracks
