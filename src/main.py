from repository import Repository

def main():
    fileName = "src/playlists/Ipizza.xml"
    playlistName = "Ipizza"

    playlist = Repository().get_playlist(fileName, playlistName)
    print(playlist.tracks[4].artist)
    

if __name__ == "__main__":
    main()