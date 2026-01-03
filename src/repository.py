import plistlib
from model.track import Track
from model.playlist import Playlist

class Repository:

    def get_playlist(self, fileName, playlistName):
        file = self.__open_file(fileName)
        file_tracks = self.__get_tracks_in_file(file)
        file_playlist = self.__find_playlist_in_file(file, playlistName)
        playlist = self.__construct_playlist(file_playlist, file_tracks, playlistName)
        return playlist
            

    def __construct_playlist(self, playlist, tracks, playlistName):
        playlist_tracks = []
        for item in playlist.get("Playlist Items", []):
            id = item.get("Track ID")
            info = tracks.get(str(id), {})
            if not info:
                raise ValueError(f"Track with ID '{id}' not found in playlist '{playlistName}'")
            
            playlist_tracks.append(
                Track(
                    title=info["Name"],
                    artist=info["Artist"],
                    duration=info["Total Time"],
                )
            )
        
        return Playlist(name=playlistName, tracks=playlist_tracks)
    

    def __get_tracks_in_file(self, file):
        return file.get("Tracks", {})
    
    
    def __find_playlist_in_file(self, file, playlistName):
        playlists = file.get("Playlists", [])
        
        for playlist in playlists:
            if playlist.get("Name") == playlistName:
                return playlist
        
        raise ValueError(f"Playlist '{playlistName}' not found in file")

          
    def __open_file(self, fileName):
        with open(fileName, "rb") as fp:
            return plistlib.load(fp)