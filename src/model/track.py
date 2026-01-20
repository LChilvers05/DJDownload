from __future__ import annotations

from datetime import datetime


class Track:
    def __init__(
        self,
        id: int,
        title: str = "",
        artist: str = "",
        duration: int = 0,
        album: str | None = None,
        album_artist: str | None = None,
        composer: str | None = None,
        genre: str | None = None,
        kind: str | None = None,
        size: int | None = None,
        disc_number: int | None = None,
        disc_count: int | None = None,
        year: int | None = None,
        track_number: int | None = None,
        track_count: int | None = None,
        date_modified: datetime | None = None,
        date_added: datetime | None = None,
        bit_rate: int | None = None,
        sample_rate: int | None = None,
        play_count: int | None = None,
        play_date: int | None = None,
        play_date_utc: datetime | None = None,
        skip_count: int | None = None,
        skip_date: datetime | None = None,
        release_date: datetime | None = None,
        normalization: int | None = None,
        artwork_count: int | None = None,
        sort_album: str | None = None,
        sort_artist: str | None = None,
        sort_name: str | None = None,
        persistent_id: str | None = None,
        track_type: str | None = None,
        protected: bool | None = None,
        apple_music: bool | None = None,
        playlist_only: bool | None = None,
        location: str | None = None,
        file_folder_count: int | None = None,
        library_folder_count: int | None = None,
        itunes_metadata: dict | None = None,
    ):
        self.id = id
        self.title = title
        self.artist = artist
        self.duration = duration

        self.album = album
        self.album_artist = album_artist
        self.composer = composer
        self.genre = genre
        self.kind = kind
        self.size = size
        self.disc_number = disc_number
        self.disc_count = disc_count
        self.year = year
        self.track_number = track_number
        self.track_count = track_count

        self.date_modified = date_modified
        self.date_added = date_added
        self.bit_rate = bit_rate
        self.sample_rate = sample_rate
        self.play_count = play_count
        self.play_date = play_date
        self.play_date_utc = play_date_utc
        self.skip_count = skip_count
        self.skip_date = skip_date
        self.release_date = release_date
        self.normalization = normalization
        self.artwork_count = artwork_count

        self.sort_album = sort_album
        self.sort_artist = sort_artist
        self.sort_name = sort_name
        self.persistent_id = persistent_id

        self.track_type = track_type
        self.protected = protected
        self.apple_music = apple_music
        self.playlist_only = playlist_only

        self.location = location
        self.file_folder_count = file_folder_count
        self.library_folder_count = library_folder_count

        self.itunes_metadata = itunes_metadata
    

    @classmethod
    def from_dict(cls, data: dict) -> Track:
        return cls(
            id=data.get("Track ID"),
            title=data.get("Name", ""),
            artist=data.get("Artist", ""),
            duration=data.get("Total Time", 0),
            album=data.get("Album"),
            album_artist=data.get("Album Artist"),
            composer=data.get("Composer"),
            genre=data.get("Genre"),
            kind=data.get("Kind"),
            size=data.get("Size"),
            disc_number=data.get("Disc Number"),
            disc_count=data.get("Disc Count"),
            year=data.get("Year"),
            track_number=data.get("Track Number"),
            track_count=data.get("Track Count"),
            date_modified=data.get("Date Modified"),
            date_added=data.get("Date Added"),
            bit_rate=data.get("Bit Rate"),
            sample_rate=data.get("Sample Rate"),
            play_count=data.get("Play Count"),
            play_date=data.get("Play Date"),
            play_date_utc=data.get("Play Date UTC"),
            skip_count=data.get("Skip Count"),
            skip_date=data.get("Skip Date"),
            release_date=data.get("Release Date"),
            normalization=data.get("Normalization"),
            artwork_count=data.get("Artwork Count"),
            sort_album=data.get("Sort Album"),
            sort_artist=data.get("Sort Artist"),
            sort_name=data.get("Sort Name"),
            persistent_id=data.get("Persistent ID"),
            track_type=data.get("Track Type"),
            protected=data.get("Protected"),
            apple_music=data.get("Apple Music"),
            playlist_only=data.get("Playlist Only"),
            location=data.get("Location"),
            file_folder_count=data.get("File Folder Count"),
            library_folder_count=data.get("Library Folder Count"),
            itunes_metadata=data,
        )
    
    def to_dict(self) -> dict:
        info: dict = dict(getattr(self, "itunes_metadata", None) or {})

        def set_if_not_none(key: str, value) -> None:
            if value is not None:
                info[key] = value

        def set_if_nonempty_str(key: str, value: str | None) -> None:
            if value is not None and value != "":
                info[key] = value

        info["Track ID"] = int(self.id)
        info["Name"] = self.title or ""
        info["Artist"] = self.artist or ""
        info["Total Time"] = int(self.duration or 0)

        set_if_nonempty_str("Album", self.album)
        if self.album_artist is not None and self.album_artist != "":
            info["Album Artist"] = self.album_artist
        elif (self.artist or "") != "" and "Album Artist" not in info:
            info["Album Artist"] = self.artist

        set_if_nonempty_str("Composer", self.composer)
        set_if_nonempty_str("Genre", self.genre)
        set_if_nonempty_str("Kind", self.kind)

        set_if_not_none("Size", self.size)
        set_if_not_none("Disc Number", self.disc_number)
        set_if_not_none("Disc Count", self.disc_count)
        set_if_not_none("Year", int(self.year) if self.year is not None else None)
        set_if_not_none("Track Number", int(self.track_number) if self.track_number is not None else None)
        set_if_not_none("Track Count", int(self.track_count) if self.track_count is not None else None)

        set_if_not_none("Date Modified", self.date_modified)
        set_if_not_none("Date Added", self.date_added)
        set_if_not_none("Bit Rate", self.bit_rate)
        set_if_not_none("Sample Rate", self.sample_rate)
        set_if_not_none("Play Count", self.play_count)
        set_if_not_none("Play Date", self.play_date)
        set_if_not_none("Play Date UTC", self.play_date_utc)
        set_if_not_none("Skip Count", self.skip_count)
        set_if_not_none("Skip Date", self.skip_date)
        set_if_not_none("Release Date", self.release_date)
        set_if_not_none("Normalization", self.normalization)
        set_if_not_none("Artwork Count", self.artwork_count)

        set_if_nonempty_str("Sort Album", self.sort_album)
        set_if_nonempty_str("Sort Artist", self.sort_artist)
        set_if_nonempty_str("Sort Name", self.sort_name)
        set_if_nonempty_str("Persistent ID", self.persistent_id)

        if self.location:
            info["Location"] = self.location
            info["Track Type"] = self.track_type or "File"
        else:
            set_if_nonempty_str("Track Type", self.track_type)

        set_if_not_none("Protected", self.protected)
        set_if_not_none("Apple Music", self.apple_music)

        info["Playlist Only"] = True if self.playlist_only is None else bool(self.playlist_only)

        set_if_not_none("File Folder Count", self.file_folder_count)
        set_if_not_none("Library Folder Count", self.library_folder_count)

        return info