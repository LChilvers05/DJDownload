from repository import Repository
from pathlib import Path

def create_track_files(repo: Repository, output_dir="output/"):
    for playlist_file in Path("playlists").glob('*.xml'):
        playlist_name = playlist_file.name.split('.xml')[0]

        audio_file = f"audio/{playlist_name}.wav"
        audio = repo.get_audio(audio_file)
        print(f"Loaded raw audio from '{audio_file}'")

        playlist = repo.get_playlist(playlist_file, playlist_name)
        print(f"Fetched playlist '{playlist.name}' with {len(playlist.tracks)} tracks")
        
        tracks = split_audio(audio, playlist)
        playlist_output_dir = f"{output_dir}/{playlist.name}"
        repo.save_tracks(tracks, playlist.tracks, playlist_output_dir)


def split_audio(raw_audio, playlist):
    audios = []
    start = 0
    for track in playlist.tracks:
        end = start + track.duration
        audio = raw_audio[start:end]
        audios.append(audio)
        start = end

    return audios


def main():
    repo = Repository()
    create_track_files(repo)


if __name__ == "__main__":
    main()
