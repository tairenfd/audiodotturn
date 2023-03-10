"""
database.py
-----------

Classes
-------
- `Database`

Notes
-----
None.
"""
import sqlite3
from audiodotturn.config import Config
from audiodotturn.errors import AudiodotturnError

class Database:
    """
    Class for creating and managing a SQLite database.

    Attributes:
        conn (sqlite3.Connection): A connection object for the database.
        c (sqlite3.Cursor): A cursor object for the database.

    Methods:
        add_data_to_db(data: dict) -> None:
            Adds data to the database.

        close_db() -> None:
            Closes the database connection.
    """
    # Connect to SQLite database
    def __init__(self, config: Config):
        """
        Initializes a new Database object.

        Args:
            database_path (str): The path to the SQLite database.

        Returns:
            None
        """
        database_path = config.program_defaults.database
        try:
            if not database_path.endswith(".db"):
                raise TypeError
        except TypeError as error:
            AudiodotturnError(error, tuple(config.program_defaults.exts), config.console)

        self.conn = sqlite3.connect(database_path)
        self.c = self.conn.cursor()

        # Create table for artists and tracks
        self.c.execute('''CREATE TABLE IF NOT EXISTS artists
                    (name TEXT PRIMARY KEY)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS tracks
                    (title TEXT, features TEXT, misc TEXT, youtube_id TEXT, filetype TEXT,
                    artist_name TEXT, FOREIGN KEY(artist_name) REFERENCES artists(name))''')

    def add_data_to_db(self, data: dict):
        """
        Adds data to the database.

        Args:
            data (dict): A dictionary containing the data to add to the database.

        Returns:
            None
        """
        # Loop through each item in the input data
        # Get the artist and track data from the item
        artist = data['artist'].lower()
        title = data['title'].lower()
        features = data['features'].lower()
        misc = data['misc'].lower()
        filetype = data['filetype'].lower()
        youtube_id = data.get('youtube_id') or None
        # Check if the artist already exists in the database
        self.c.execute("SELECT * FROM artists WHERE LOWER(name)=?", (artist,))
        artist_row = self.c.fetchone()

        if artist_row is None:
            # If the artist doesn't exist, add a new entry to the artists table
            self.c.execute("INSERT INTO artists (name) VALUES (?)", (artist,))
            self.conn.commit()

        # Check if the track already exists for the artist
        self.c.execute("SELECT * FROM tracks WHERE LOWER(title)=? AND LOWER(artist_name)=?", (title, artist))
        track_row = self.c.fetchone()

        if track_row is None:
            # If the track doesn't exist, add a new entry to the tracks table
            self.c.execute("INSERT INTO tracks (title, features, misc, youtube_id, filetype, artist_name) VALUES (?, ?, ?, ?, ?, ?)",
                    (title, features, misc, youtube_id, filetype, artist))
            self.conn.commit()

    def close_db(self):
        """
        Closes the database connection.

        Returns:
            None
        """
        self.conn.close()
