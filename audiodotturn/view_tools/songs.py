import sqlite3
from rich.console import Console
from audiodotturn.errors import AudiodotturnError

class Song:
    """
    A class that provides functionality for viewing the list of songs.

    Args:
        conn (sqlite3.Connection): a connection to the SQLite database
        query (str): search query
    """
    def __init__(self, cursor: sqlite3.Connection.cursor):
        self.c = cursor
        self.query = ""

    def _search(self, search_key: str):
        '''
        Search through 'search_key' category of tracks to find matches for 'query'

        Args:
            search_key (str): the category to search within
        
        Returns:
            results (list): returns a list of the search results
        '''
        results = []
        try:
            self.c.execute(f"SELECT tracks.title, tracks.features, tracks.misc, tracks.youtube_id, tracks.filetype, artists.name FROM tracks JOIN artists ON tracks.artist_name=artists.name WHERE {search_key} LIKE ?", ('%' + self.query + '%',))
        except sqlite3.OperationalError as error:
            AudiodotturnError(error, ("error",), Console(), if_exit=True)
        rows = self.c.fetchall()
        for row in rows:
            track_info = {
                'artist': row[5],
                'title': row[0],
                'features': row[1],
                'misc': row[2],
                'youtube_id': row[3],
                'filetype': row[4]
            }
            results.append(track_info)
        return results

    def search_by_artist(self, query: str) -> list:
        """
        Returns:
            list: a list of dictionaries containing the info for all songs by a specified artist in the database.
        """
        self.query = query
        return self._search('artists.name')

    def search_by_title(self, query: str) -> list:
        """
        Returns:
            list: a list of dictionaries containing the info for all songs with a specified title/name in the database.
        """
        self.query = query
        return self._search('tracks.title')

    def search_by_features(self, query: str) -> list:
        """
        Returns:
            list: a list of dictionaries containing the info for all songs with specified features in the database.
        """
        self.query = query
        return self._search('tracks.features')

    def search_by_misc(self, query: str) -> list:
        """
        Returns:
            list: a list of dictionaries containing the info for all songs with specified misc info in the database.
        """
        self.query = query
        return self._search('tracks.misc')

    def search_by_youtube_id(self, query: str) -> list:
        """
        Returns:
            list: a list of dictionaries containing the info for all songs with a specified YouTube ID in the database.
        """
        self.query = query
        return self._search('tracks.youtube_id')

    def search_by_filetype(self, query: str) -> list:
        """
        Returns:
            list: a list of dictionaries containing the info for all songs with a specified file type in the database.
        """
        self.query = query
        return self._search('tracks.filetype')
