from model.track import Track

class Playlist:
    def __init__(self, name: str, tracks: list[Track]):
        self.name = name
        self.tracks = tracks