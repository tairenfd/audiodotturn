import sqlite3
from typing import List, Dict

class DatabaseInit:
    def __init__(self, path: str) -> None:
        """
        Constructs a new Database object.

        Parameters:
            path : str
                A string representing the file path of the database. Database must be a `.db` file.
        """
        self.path = path if path.endswith('.db') else None
        if self.path is None:
            raise TypeError("Database must be a .db file")


class DatabaseCreate(DatabaseInit):
    def create_database(self) -> None:
        """
        Creates a new database file at the specified path if it does not exist.
        """
        try:
            conn = sqlite3.connect(self.path)
            conn.close()
        except:
            raise sqlite3.OperationalError(f'Could not create database in {self.path}')

    def create_tables(self) -> None:
        """
        Creates the necessary tables for the database.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                artist_id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY,
                title TEXT,
                features TEXT,
                misc TEXT,
                youtube_id TEXT,
                file_extension TEXT,
                artist_id INTEGER,
                FOREIGN KEY(artist_id) REFERENCES artist(artist_id)
            )
        """)

        conn.commit()
        conn.close()


class DatabaseRead(DatabaseInit):
    def get_all_artists(self) -> List[Dict]:
        """
        Retrieves a list of all artists in the database.

        Returns:
            A list of dictionaries representing each artist in the database,
            with keys 'artist_id' and 'name'.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT artist_id, name FROM artists')
        result = cursor.fetchall()
        conn.close()
        if result:
            return [{'artist_id': row[0], 'name': row[1]} for row in result]
        return None

    def get_artist_by_id(self, artist_id: int) -> Dict:
        """
        Retrieves the artist with the given ID from the database.

        Parameters:
            artist_id : int
                The ID of the artist to retrieve.

        Returns:
            A dictionary representing the artist in the database,
            with keys 'artist_id' and 'name'.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT artist_id, name FROM artists WHERE artist_id = ?', (artist_id,))
        result = cursor.fetchall()
        conn.close()
        if result:
            return [{'artist_id': row[0], 'name': row[1]} for row in result]
        return None

    def get_songs_by_artist_by_id(self, artist_id: int) -> List[Dict]:
        """
        Retrieves a list of all songs by the artist with the given ID from the database.

        Parameters:
            artist_id : int
                The ID of the artist whose songs to retrieve.

        Returns:
            A list of dictionaries representing each song by the artist in the database,
            with keys 'song_id', 'title', 'features', 'misc', 'youtube_id', and 'file_extension'.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT song_id, title, features, misc, youtube_id, file_extension '
                    'FROM songs WHERE artist_id = ?', (artist_id,))
        result = cursor.fetchall()
        conn.close()
        if result:
            return [{'song_id': row[0], 'title': row[1], 'features': row[2],
                    'misc': row[3], 'youtube_id': row[4], 'file_extension': row[5]} for row in result if row]
        return None

    def get_song_by_id(self, song_id: int) -> Dict:
        """
        Retrieves the song with the given ID from the database.

        Parameters:
            song_id : int
                The ID of the song to retrieve.

        Returns:
            A dictionary representing the song in the database,
            with keys 'song_id', 'title', 'features', 'misc', 'youtube_id', and 'file_extension'.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT song_id, title, features, misc, youtube_id, file_extension '
                    'FROM songs WHERE song_id = ?', (song_id,))
        result = cursor.fetchall()[0]
        conn.close()
        if result:
            return {'song_id': result[0], 'title': result[1], 'features': result[2],
                    'misc': result[3], 'youtube_id': result[4], 'file_extension': result[5]}
        return None


class DatabaseUpdate(DatabaseInit):
    def update_database(self, data: List[Dict]) -> None:
        """
        Updates the database with the provided data from an extractor.
        If the artist exists, the data is added as a new song for that artist.
        If the artist does not exist, a new artist entry is created and the data is added as the first song.
        If the song already exists, any missing information is updated without changing existing information.

        Parameters:
            data : list of dicts
                A list of dicts representing the extracted music metadata:
                the original filename, the artist info, title info, features info, misc info, youtube_id info,
                the file extension, and the extraction status value (True or False).
        Returns:
            tuple : (new_artists, new_songs, updated, failure)
                Stats of last update run
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        new_artists = 0
        new_songs = 0
        updated = 0
        failure = 0


        for row in data:
            if not row["status"]:
                failure += 1
                continue

            artist_name = row["artist"].lower()
            song_title = row["title"]
            features = row["features"]
            misc = row["misc"]
            youtube_id = row["youtube_id"]
            file_extension = row["filetype"]

            # check if artist exists in database
            try:
                cursor.execute('SELECT artist_id FROM artists WHERE name = ?', (artist_name,))
                result = cursor.fetchone()

            except sqlite3.OperationalError:
                result = False

            if result:
                artist_id = result[0]
                cursor.execute('SELECT song_id, features, misc, youtube_id FROM songs WHERE title = ? AND artist_id = ?',
                            (song_title, artist_id))
                result = cursor.fetchone()
                if result:
                    check = False
                    song_id = result[0]
                    # update only the missing information for the existing song
                    if result[1] is None:
                        check = True
                        cursor.execute('UPDATE songs SET features = ? WHERE song_id = ?', (features, song_id))
                    if result[2] is None:
                        check = True
                        cursor.execute('UPDATE songs SET misc = ? WHERE song_id = ?', (misc, song_id))
                    if result[3] is None:
                        check = True
                        cursor.execute('UPDATE songs SET youtube_id = ? WHERE song_id = ?', (youtube_id, song_id))
                    if check:
                        updated += 1
                else:
                    # add a new song for the artist
                    cursor.execute('INSERT INTO songs (artist_id, title, features, misc, youtube_id, file_extension) '
                                'VALUES (?, ?, ?, ?, ?, ?)', (artist_id, song_title, features, misc, youtube_id, file_extension))
                    new_songs += 1
            else:
                # add a new artist and song
                cursor.execute('INSERT INTO artists (name) VALUES (?)', (artist_name,))
                artist_id = cursor.lastrowid
                cursor.execute('INSERT INTO songs (artist_id, title, features, misc, youtube_id, file_extension) '
                            'VALUES (?, ?, ?, ?, ?, ?)', (artist_id, song_title, features, misc, youtube_id, file_extension))
                new_songs += 1
                new_artists += 1

        conn.commit()
        conn.close()
        return new_artists, new_songs, updated, failure


class Database(DatabaseCreate, DatabaseRead, DatabaseUpdate):
    """
    Subclass of all Database Classes, usually what will be instantiated.
    """
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
