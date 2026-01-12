import plistlib
from pydub import AudioSegment
from pathlib import Path
from mutagen.aiff import AIFF
from mutagen.id3 import TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON
from model.track import Track
from model.playlist import Playlist

class Repository:

    def get_audio(self, path: Path):
        return AudioSegment.from_file(path, format="wav")
    

    def get_playlist(self, file_name, playlist_name):
        file = self.__open_playlist_file(file_name)
        file_tracks = self.__get_tracks_in_playlist_file(file)
        file_playlist = self.__find_playlist_in_playlist_file(file, playlist_name)
        playlist = self.__construct_playlist(file_playlist, file_tracks, playlist_name)
        
        return playlist

    
    def save_track(self, track: AudioSegment, metadata: Track, path: Path):
        path.mkdir(exist_ok=True)
        track_path = path / f"{metadata.title}.aiff"
        track.export(track_path, format="aiff")
        self.__add_track_metadata(track_path, metadata)


    def __add_track_metadata(self, path, metadata: Track):
        aiff = AIFF(path)
        if aiff.tags is None:
            aiff.add_tags()

        aiff.tags.add(TIT2(encoding=3, text=metadata.title))
        aiff.tags.add(TPE1(encoding=3, text=metadata.artist))
        if metadata.album:
            aiff.tags.add(TALB(encoding=3, text=metadata.album))
        if metadata.album_artist:
            aiff.tags.add(TPE2(encoding=3, text=metadata.album_artist))
        if metadata.genre:
            aiff.tags.add(TCON(encoding=3, text=metadata.genre))
        if metadata.year:
            aiff.tags.add(TDRC(encoding=3, text=str(metadata.year)))
        if metadata.track_number:
            track_text = str(metadata.track_number)
            if metadata.track_count:
                track_text += f"/{metadata.track_count}"
            aiff.tags.add(TRCK(encoding=3, text=track_text))

        aiff.save()
            

    def __construct_playlist(self, playlist, tracks, playlist_name):
        playlist_tracks = []
        for item in playlist.get("Playlist Items", []):
            id = item.get("Track ID")
            info = tracks.get(str(id), {})
            if not info:
                raise ValueError(f"Track with ID '{id}' not found in playlist '{playlist_name}'")
            
            playlist_tracks.append(
                Track(
                    title=info["Name"],
                    artist=info["Artist"],
                    duration=info["Total Time"],
                    album=info.get("Album"),
                    album_artist=info.get("Album Artist"),
                    genre=info.get("Genre"),
                    year=info.get("Year"),
                    track_number=info.get("Track Number"),
                    track_count=info.get("Track Count"),
                )
            )
        
        return Playlist(name=playlist_name, tracks=playlist_tracks)
    

    def __get_tracks_in_playlist_file(self, file):
        return file.get("Tracks", {})
    
    
    def __find_playlist_in_playlist_file(self, file, playlist_name):
        playlists = file.get("Playlists", [])
        
        for playlist in playlists:
            if playlist.get("Name") == playlist_name:
                return playlist
        
        raise ValueError(f"Playlist '{playlist_name}' not found in file")

          
    def __open_playlist_file(self, file_name):
        with open(file_name, "rb") as fp:
            return plistlib.load(fp)
