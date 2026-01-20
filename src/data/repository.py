import plistlib
from pydub import AudioSegment
from pathlib import Path
from mutagen.aiff import AIFF
from mutagen.id3 import TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON
from model.track import Track
from model.playlist import Playlist
import plistlib
import uuid
from datetime import datetime, timezone

class Repository:

    def get_audio(self, path: Path):
        return AudioSegment.from_file(path, format="wav")
    
    
    def get_playlists(self) -> list[Playlist]:
        playlists = []
        for playlist_file in self.__get_playlist_files():
            playlist_name = playlist_file.name.split('.xml')[0]
            playlist = self.get_playlist(playlist_file, playlist_name)
            print(f"Fetched playlist '{playlist.name}' with {len(playlist.tracks)} tracks")
            playlists.append(playlist)

        return playlists
    

    def get_playlist(self, file_name: Path, playlist_name: str) -> Playlist:
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

    
    def save_playlist_to_file(self, playlist: Playlist):

        def persistent_id_from_name(name: str) -> str:
            return uuid.uuid5(uuid.NAMESPACE_DNS, name).hex[:16].upper()

        output_file_name = f"#{playlist.name}.xml"
        output_path: Path = Path("output") / output_file_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        tracks_dict: dict[str, dict] = {}
        for track in playlist.tracks:
            tracks_dict[str(int(track.id))] = track.to_dict()

        playlist_id = abs(hash(playlist.name)) % 10_000_000 or 1
        playlist_persistent_id = persistent_id_from_name(playlist.name)
        library_persistent_id = persistent_id_from_name("DJDownload")

        plist_root: dict = {
            "Major Version": 1,
            "Minor Version": 1,
            "Date": datetime.now(timezone.utc),
            "Application Version": "1.5.6.11",
            "Features": 5,
            "Show Content Ratings": True,
            "Music Folder": "file:///Users/leechilvers/Music/iTunes/iTunes%20Media/",
            "Library Persistent ID": library_persistent_id,
            "Tracks": tracks_dict,
            "Playlists": [
                {
                    "Name": output_file_name,
                    "Description": "",
                    "Playlist ID": int(playlist_id),
                    "Playlist Persistent ID": playlist_persistent_id,
                    "All Items": True,
                    "Playlist Items": [{"Track ID": int(t.id)} for t in playlist.tracks],
                }
            ],
        }

        with open(output_path, "wb") as fp:
            plistlib.dump(plist_root, fp, fmt=plistlib.FMT_XML, sort_keys=False)


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

    
    def __get_playlist_files(self):
        return Path("playlists").glob('*.xml')
    

    def __open_playlist_file(self, file_name):
        with open(file_name, "rb") as fp:
            return plistlib.load(fp)
        

    def __get_tracks_in_playlist_file(self, file):
        return file.get("Tracks", {})
    
    
    def __find_playlist_in_playlist_file(self, file, playlist_name):
        playlists = file.get("Playlists", [])
        
        for playlist in playlists:
            if playlist.get("Name") == playlist_name:
                return playlist
        
        raise ValueError(f"Playlist '{playlist_name}' not found in file")
    
    
    def __construct_playlist(self, playlist, tracks, playlist_name):
        playlist_tracks = []
        for item in playlist.get("Playlist Items", []):
            id = item.get("Track ID")
            info = tracks.get(str(id), {})
            if not info:
                raise ValueError(f"Track with ID '{id}' not found in playlist '{playlist_name}'")
            
            playlist_tracks.append(Track.from_dict(info))
        
        return Playlist(name=playlist_name, tracks=playlist_tracks)
