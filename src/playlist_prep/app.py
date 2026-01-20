from data.repository import Repository
from model.track import Track

class App:

    def __init__(self, repo: Repository):
        self.repo = repo

    def run(self):

        silence_track = Track(
            id=27210,
            title="Silence", 
            artist="",
            duration=0,
            location="file:///Users/leechilvers/Music/iTunes/iTunes%20Media/Music/Unknown%20Artist/Unknown%20Album/silence.mp3"
        )

        for playlist in self.repo.get_playlists():
            for i in range(1, len(playlist.tracks)*2, 2):
                playlist.tracks.insert(i, silence_track)

            self.repo.save_playlist_to_file(playlist)
            print(f"Prepped playlist '{playlist.name}' with {len(playlist.tracks)} items")









