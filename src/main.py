from repository import Repository
from pathlib import Path

"""TODO: a better approach to this project is to slide through audio and slice
    in the middle of silences, rather than slicing strictly by duration.
    This will require analyzing the audio to find silence points.
    Reject outliers where the length of the silence could not possible be the length of a song
"""

def create_track_files(repo: Repository):
    for playlist_file in Path("playlists").glob('*.xml'):
        playlist_name = playlist_file.name.split('.xml')[0]

        audio_path = Path(f"audio/{playlist_name}.wav")
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file '{audio_path.name}' not found")

        playlist = repo.get_playlist(playlist_file, playlist_name)
        print(f"Fetched playlist '{playlist.name}' with {len(playlist.tracks)} tracks")

        start = 0
        for track_metadata in playlist.tracks:
            duration = track_metadata.duration
            slice = repo.get_audio_slice(
                audio_path=audio_path, 
                start=start, 
                duration=duration
            )

            repo.save_track(
                track=slice, 
                metadata=track_metadata, 
                path=Path("output") / playlist.name
            )
            print(f"Saved track '{track_metadata.title}'")

            start = start + duration


def main():
    repo = Repository()
    create_track_files(repo)


if __name__ == "__main__":
    main()
