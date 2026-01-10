class Track:
    def __init__(self, title: str, artist: str, duration: int, album: str = None, 
                 album_artist: str = None, genre: str = None, year: int = None, 
                 track_number: int = None, track_count: int = None):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.album = album
        self.album_artist = album_artist
        self.genre = genre
        self.year = year
        self.track_number = track_number
        self.track_count = track_count