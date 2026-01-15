from pathlib import Path
from slicer.audio_processor import AudioProcessor
from data.repository import Repository

class App:

    def __init__(self, repo: Repository):
        self.repo = repo
        

    def run(self):
        for playlist in self.repo.get_playlists():
            temp_path = AudioProcessor().slice_audio(Path(f"audio/{playlist.name}.wav"))
            
            self.save_songs_from_slices(self.repo, temp_path, playlist)


    def save_songs_from_slices(self, repo, temp_path, playlist):
        j = 0
        for i in range(len(list(temp_path.glob('*.wav')))):
            temp_file = temp_path / f"temp_{i:03d}.wav"
            temp_audio = repo.get_audio(temp_file)
            temp_duration = len(temp_audio)

            track = playlist.tracks[j]
            if not (abs(track.duration - temp_duration) <= 5000): # 5 sec
                continue
                
            repo.save_track(
                track=temp_audio, 
                metadata=track, 
                path=Path("output") / playlist.name
            )
            print(f"Saved track '{track.title}'")
            j += 1
            
        if j != len(playlist.tracks):
            print(f"Warning: Only matched {j} out of {len(playlist.tracks)} tracks for playlist '{playlist.name}'")