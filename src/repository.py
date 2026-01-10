import plistlib
from pydub import AudioSegment
from pathlib import Path
from mutagen.aiff import AIFF
from mutagen.id3 import TIT2, TPE1, TALB, TRCK, TDRC
from model.track import Track
from model.playlist import Playlist

class Repository:

    def get_audio(self, file_name):
        return AudioSegment.from_wav(file_name)
    

    def get_playlist(self, file_name):
        name = file_name.split('/')[-1].split('.xml')[0]
        file = self.__open_file(file_name)
        file_tracks = self.__get_tracks_in_file(file)
        file_playlist = self.__find_playlist_in_file(file, name)
        playlist = self.__construct_playlist(file_playlist, file_tracks, name)
        return playlist


    def save_tracks(self, tracks, metadata, directory):
        path = Path(directory)
        path.mkdir(exist_ok=True)
        for track, meta in zip(tracks, metadata):
            self.__save_track(track, meta, path)

    
    def __save_track(self, track: AudioSegment, metadata: Track, path):
        track_path = path / f"{metadata.title}.mp3"

        print(track.sample_width)
        print(track.frame_rate)
        print(track.channels)
        track.set_channels(2)
        track.set_sample_width(4)

        track.export(out_f=metadata.title, format="mp3")
        # self.__add_track_metadata(track_path, metadata)
        print(f"Saved track '{metadata.title}'")

    
    # def __add_track_metadata(self, path, metadata: Track):
    #     aiff = AIFF(path)
    #     if aiff.tags is None:
    #         aiff.add_tags()

    #     aiff.tags.add(TIT2(encoding=3, text=metadata.title))
    #     aiff.tags.add(TPE1(encoding=3, text=metadata.artist))

    #     aiff.save()
            

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
                )
            )
        
        return Playlist(name=playlist_name, tracks=playlist_tracks)
    

    def __get_tracks_in_file(self, file):
        return file.get("Tracks", {})
    
    
    def __find_playlist_in_file(self, file, playlist_name):
        playlists = file.get("Playlists", [])
        
        for playlist in playlists:
            if playlist.get("Name") == playlist_name:
                return playlist
        
        raise ValueError(f"Playlist '{playlist_name}' not found in file")

          
    def __open_file(self, file_name):
        with open(file_name, "rb") as fp:
            return plistlib.load(fp)