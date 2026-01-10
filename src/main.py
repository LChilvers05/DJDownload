from repository import Repository

def create_track_files(playlist_file, audio_file, output_dir):
    repo = Repository()

    playlist = repo.get_playlist(playlist_file)
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


def main():
    create_track_files(
        playlist_file="playlists/Ipizza.xml",
        audio_file="audio/Ipizza.wav",
        output_dir="output/"
    )


if __name__ == "__main__":
    main()
