from data.repository import Repository
from pathlib import Path
import plistlib

class App:

    def __init__(self, repo: Repository):
        self.repo = repo


    def _find_playlist(self, plist: dict, playlist_name: str) -> dict:
        playlists = plist.get("Playlists", [])
        if not isinstance(playlists, list) or not playlists:
            raise ValueError("No playlists found in plist")

        for playlist in playlists:
            if isinstance(playlist, dict) and playlist.get("Name") == playlist_name:
                return playlist

        raise ValueError(f"Playlist '{playlist_name}' not found in plist")


    def _add_track(self, plist: dict, track_id: int, track: dict) -> None:
        tracks = plist.setdefault("Tracks", {})
        if not isinstance(tracks, dict):
            raise ValueError("plist['Tracks'] is not a dict")

        tracks[str(track_id)] = track


    def _prepend_playlist_item(self, playlist: dict, track_id: int) -> None:
        items = playlist.setdefault("Playlist Items", [])
        if not isinstance(items, list):
            raise ValueError("playlist['Playlist Items'] is not a list")

        items.insert(0, {"Track ID": track_id})


    def run(self):
        for playlist_file in self.repo.get_playlist_files():
            playlist_name = playlist_file.stem
            plist = self.repo.open_playlist_file(playlist_file)
            playlist = self._find_playlist(plist, playlist_name)

            # todo: create a silent track
            # import into music app
            # check details when exporting library again
            # use here

            name = "Silence"
            location = "file:///Users/leechilvers/Music/iTunes/iTunes%20Media/Apple%20Music/Martin%20Solveig/Places%20(feat.%20Ina%20Wroldsen)%20-%20Single/01%20Places%20(feat.%20Ina%20Wroldsen).m4p"

            track_id = self._next_track_id(plist)
            track = {
                "Track ID": track_id,
                "Name": name,
                "Artist": "",
                "Album Artist": "",
                "Album": "",
                "Genre": "",
                "Kind": "MPEG audio file",
                "Total Time": 0,
                "Track Type": "File",
                "Location": location,
                "Playlist Only": True,
            }

            self._add_track(plist, track_id, track)
            self._prepend_playlist_item(playlist, track_id)

            output_path = Path("output") / f"{playlist_name}_prep.xml"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as fp:
                plistlib.dump(plist, fp)









