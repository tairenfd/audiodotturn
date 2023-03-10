import sqlite3
from rich.console import Console
from audiodotturn.errors import AudiodotturnError

class Artist:
    """
    A class that provides functionality for viewing the list of artists.
    """
    def __init__(self, cursor: sqlite3.Connection.cursor):
        self.cursor = cursor

    def get_artists(self):
        """
        Returns:
            list: a list of all artists in the database.
        """
        self.cursor.execute("SELECT name FROM artists")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_tracks(self):
        """
        Returns:
            list: a list of all tracks and their artist in the database.
        """
        tracks_list = {}
        c = self.cursor
        try:
            c.execute("SELECT tracks.title, artists.name, tracks.features, tracks.misc, tracks.youtube_id, tracks.filetype FROM tracks JOIN artists ON tracks.artist_name=artists.name")
        except sqlite3.OperationalError as error:
            AudiodotturnError(error, ("error",), Console(), if_exit=True)
        rows = c.fetchall()
        for row in rows:
            artist = row[1]
            if artist not in tracks_list:
                tracks_list[artist] = []
            track_info = {
                'title': row[0],
                'artist': artist,
                'features': row[2],
                'misc': row[3],
                'youtube_id': row[4],
                'filetype': row[5]
            }
            tracks_list[artist].append(track_info)
        return tracks_list