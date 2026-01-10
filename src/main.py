from repository import Repository
from model.playlist import Playlist
from model.track import Track

def main():
    create_track_files(
        playlist_file="src/playlists/Ipizza.xml",
        audio_file="src/audio/Ipizza.wav",
        output_dir="../output/"
    )


def create_track_files(playlist_file, audio_file, output_dir):
    repo = Repository()

    # playlist = repo.get_playlist(playlist_file)
    playlist = Playlist(
        name="Ipizza",
        tracks=[
            Track(title="Track 1", artist="Artist A", duration=5500),
            Track(title="Track 2", artist="Artist B", duration=5500),
            Track(title="Track 3", artist="Artist C", duration=5000),
        ]
    )
    print(f"Fetched playlist '{playlist.name}' with {len(playlist.tracks)} tracks")

    audio = repo.get_audio(audio_file)
    print(f"Loaded raw audio from '{audio_file}'")

    tracks = split_audio(audio, playlist)
    repo.save_tracks(tracks, playlist.tracks, output_dir)


def split_audio(raw_audio, playlist):
    audios = []
    start = 0
    for track in playlist.tracks:
        end = start + track.duration
        audio = raw_audio[start:end]
        audios.append(audio)
        start = end

    return audios

if __name__ == "__main__":
    main()