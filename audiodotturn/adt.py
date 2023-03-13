from typing import List, Dict, Any
from audiodotturn.config import ConfigUser
from audiodotturn.construct import Constructor
from audiodotturn.extract import Extractor
from audiodotturn.database import Database


class AudioDotTurn:
    def __init__(self, config_path: str = None, db_path: str = None):
        self.config = ConfigUser(config_path)
        self.extractor = Extractor(self.config.exts, self.config.output_opts)
        self.database = Database(db_path or self.config.db_path)
        self.current_data = None
        self.constructor = None

    def extract_files(self, files: List[str], output_format: str = "dict") -> List[Any]:
        """
        Extracts metadata from multiple audio files and returns a list of dictionaries which
        contain the data or a list of the data in the chosen format.
        """
        self.current_data = self.extractor.extract_complex_list(files, output_format)
        return self.current_data

    def extract_file(self, file: str, opt: str = "dict") -> List[Any]:
        """
        Extracts metadata from a single audio file and returns a list containing a single
        dictionary containing the data.
        """
        self.extractor.complex_extract(file)
        self.current_data = self.extractor.get_extraction(opt)
        return [self.current_data]

    def update_database(self, data: List[Dict] = None) -> None:
        """
        Updates the database with data extracted from audio files.
        """
        self.database.create_database()
        self.database.create_tables()
        return self.database.update_database(data or self.current_data)
    
    def get_all_artists(self) -> List[Dict]:
        """
        Returns a list of all artists in the database.
        """
        return self.database.get_all_artists()

    def get_artist_by_id(self, artist_id: int) -> List[Dict]:
        """
        Returns a list of all artists in the database.
        """
        return self.database.get_artist_by_id(artist_id)

    def get_all_artists_and_songs(self) -> Dict:
        """
        Returns a dict of all artists and their songs in the database.
        """
        songs = {}
        artists = self.database.get_all_artists()
        for artist in artists:
            songs[artist["name"]] = self.database.get_songs_by_artist_by_id(artist["artist_id"])
        return songs

    def get_songs_by_artist(self, artist_id: int) -> List[Dict]:
        """
        Returns a list of all songs by a given artist.
        """
        return self.database.get_songs_by_artist_by_id(artist_id)

    def get_song_by_id(self, song_id: int) -> Dict:
        """
        Returns a song with the given ID.
        """
        return self.database.get_song_by_id(song_id)

    def construct(self, constructor: str, data: List[Dict] = None, auto: bool = False) -> Dict:
        """
        Constructs new audio files from the data in the database and returns a dictionary containing the
        filenames and the options used to construct them.
        """
        data = data or self.current_data
        if constructor not in self.config.constructors:
            raise TypeError(f"constructor {constructor} does not exist")
        self.constructor = Constructor(data, constructor, auto)
        self.constructor.from_dict()
        return {
            "success": self.constructor.get_success(),
            "failure": self.constructor.get_failure()
        }
