import re
import subprocess
from pathlib import Path
import shutil

class AudioProcessor:
    def __init__(self, temp_dir: Path | str = "temp"):
        self.temp_dir = Path(temp_dir)
    

    def slice_audio(self, audio_path: Path | str, threshold: int = -80, duration: float = 2.0) -> Path:
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file '{audio_path.name}' not found")

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir()

        silence_times = self.__detect_audio(audio_path, threshold, duration)
        if not silence_times:
            raise RuntimeError("No silence detected")

        segment_times = ",".join(silence_times)

        cmd = [
            "ffmpeg",
            "-i",
            str(audio_path),
            "-f",
            "segment",
            "-segment_times",
            segment_times,
            "-reset_timestamps",
            "1",
            str(self.temp_dir / "temp_%03d.wav"),
        ]

        subprocess.run(cmd, check=True)
        print("Audio slicing completed successfully")

        return self.temp_dir
    

    def __detect_audio(self, audio_path: Path | str, threshold: int, duration: float) -> list[str]:
        audio_path = Path(audio_path)

        cmd = [
            "ffmpeg",
            "-i",
            str(audio_path),
            "-af",
            f"silencedetect=noise={threshold}dB:d={duration}",
            "-f",
            "null",
            "-",
        ]

        result = subprocess.run(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            text=True,
            check=True,
        )

        silence_ends: list[str] = []
        for line in result.stderr.splitlines():
            match = re.search(r"silence_end: ([0-9.]+)", line)
            if match:
                silence_ends.append(match.group(1))

        return silence_ends
