from repository import Repository
from pathlib import Path
from audio_processor import AudioProcessor

def create_track_files(repo: Repository):

    for playlist_file in Path("playlists").glob('*.xml'):
        playlist_name = playlist_file.name.split('.xml')[0]

        temp_path = AudioProcessor().slice_audio(Path(f"audio/{playlist_name}.wav"))

        playlist = repo.get_playlist(playlist_file, playlist_name)
        print(f"Fetched playlist '{playlist.name}' with {len(playlist.tracks)} tracks")
        
        save_songs_from_slices(repo, temp_path, playlist)


def save_songs_from_slices(repo, temp_path, playlist):
    j = 0
    for i in range(len(list(temp_path.glob('*.wav')))):
        temp_file = temp_path / f"temp_{i:03d}.wav"
        temp_audio = repo.get_audio(temp_file)
        temp_duration = len(temp_audio)

        track = playlist.tracks[j]
        if not (abs(track.duration - temp_duration) <= 5000): # 5 sec
            continue
            
        repo.save_track(
            track=temp_audio, 
            metadata=track, 
            path=Path("output") / playlist.name
        )
        print(f"Saved track '{track.title}'")
        j += 1
        
    if j != len(playlist.tracks):
        print(f"Warning: Only matched {j} out of {len(playlist.tracks)} tracks for playlist '{playlist.name}'")


def main():
    repo = Repository()
    create_track_files(repo)


if __name__ == "__main__":
    main()
