from repository import Repository

def main():
    fileName = "src/playlists/Ipizza.xml"
    playlistName = "Ipizza"

    playlist = Repository().get_playlist(fileName, playlistName)
    print(playlist.tracks[0].title, playlist.tracks[0].artist, playlist.tracks[0].duration)
    

if __name__ == "__main__":
    main()