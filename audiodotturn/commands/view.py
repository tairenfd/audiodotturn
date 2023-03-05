import os
import json
import argparse
from rich.markdown import Markdown
from audiodotturn.config import Config
from audiodotturn.errors import error_handler


class View(Config):
    """
    A class that provides functionality for viewing the contents of the dataset.
    """
    def __init__(self, args: argparse.Namespace):
        """
        Initialize View class

        Args:
            args: An argparse.Namespace object containing the command line arguments passed to the Create class object.

        Returns:
            None
        """
        self.args = args
        # get defaults
        super().__init__()
        self.msg = ''
        # set user defined args
        if self.args.view_command == 'songs':
            self.artist = self.args.artist if self.args.artist else ''
            self.id = self.args.id if self.args.id else ''
            self.name = self.args.name if self.args.name else ''
        # attempt to open the given dataset
        try:
            with open(os.path.join(self.args.data), 'r', encoding='utf-8') as f:
                self.dataset = json.load(f, object_hook=dict)
        except IOError as error:
            self.dataset = {}
            error_handler(self.error_msg, self.console, error)

    # view command runner
    def run(self) -> None:
        """
        Run the View class.

        Args:
            None

        Returns:
            None
        """
        with self.console.status("[bold green]Working..."):
            if self.args.view_command == 'artists':
                if self.args.tracks:
                    self.msg = self.get_artists_tracks()
                elif self.args.names:
                    self.msg = self.get_artists()

            elif self.args.view_command == 'songs':
                if self.args.artist:
                    self.artist = self.args.artist
                    self.msg = self.get_songs_by_artist()
                elif self.args.id:
                    self.id = self.args.id
                    self.msg = self.get_songs_by_id()
                elif self.args.name:
                    self.name = self.args.name
                    self.msg = self.get_songs_by_name()
            else:
                self.msg = self.args.view_command

            self.console.log(Markdown(self.msg))

    # View - artists commands
    def get_artists(self) -> str:
        """
        Returns:
            str: a formatted string containing a list of all artists in the dataset.
        """        
        # get list of all artists in dataset
        artists_list = []
        for artist in self.dataset:
            artists_list.append(f'                            - {artist}')

        return f"# Database: {self.filename}\n\n" + "## Artists:\n" + '\n'.join(artists_list)

    def get_artists_tracks(self) -> str:
        """
        Returns:
            str: a formatted string containing a list of all the artists and their songs in the dataset.
        """
        # get list of all artists and their tracks in dataset
        artists_list = []
        for artist in self.dataset:
            artists_list.append(f'### Artist: **{artist}**')
            for tracks in self.dataset[artist]['tracks']:
                msg = f'''#### Track: {tracks["title"]}
                            - Artist: {artist}
                            - Features: {tracks["features"]}
                            - Misc: {tracks["misc"]}
                            - YouTube ID: {tracks["youtube_id"]}
                            - File Type: {tracks["filetype"]}\n'''
                artists_list.append(msg)

        return f"# Database: {self.filename}\n\n" + "## Artists and their Tracks:\n" + '\n'.join(artists_list)

    # View - songs commands
    def get_songs_by_artist(self) -> str:
        """
        Returns:
            str: a formatted string containing a list of all songs by a specified artist in the dataset.
        """
        # get list of all songs by an artist (will search by substring) name in dataset
        artists_list = []
        for artist_key in self.dataset.keys():
            if self.artist.lower() in artist_key.lower():
                for track in self.dataset[artist_key]['tracks']:
                    msg = f'''#### **{track["title"]}**
                                - Artist: {artist_key}
                                - Features: {track["features"]}
                                - Misc: {track["misc"]}
                                - YouTube ID: {track["youtube_id"]}
                                - File Type: {track["filetype"]}\n'''
                    artists_list.append(msg)

        return f"# Database: {self.filename}\n\n" + f"## Songs by artist matching '{self.artist}':\n" + '\n'.join(artists_list)

    def get_songs_by_id(self) -> str:
        """
        Returns:
            str: a formatted string containing a list of all songs by a specified youtube_id in the 
        dataset.
        """
        # get list of all songs by their youtube id in dataset
        artists_list = []
        for artist_key in self.dataset.keys():
            for track in self.dataset[artist_key]['tracks']:
                if self.youtube_id in track['youtube_id']:
                    msg = f'''#### **{track["title"]}**
                                - Artist: {artist_key}
                                - Features: {track["features"]}
                                - Misc: {track["misc"]}
                                - YouTube ID: {track["youtube_id"]}
                                - File Type: {track["filetype"]}\n'''
                    artists_list.append(msg)

        return f"# Database: {self.filename}\n\n" + f"## Songs by ID {self.youtube_id}:\n" + '\n'.join(artists_list)

    def get_songs_by_name(self) -> str:
        """
        Returns:
            str: a formatted string containing a list of all songs by a specified title/name in the 
        dataset.
        """
        artists_list = []
        for artist_key in self.dataset.keys():
            for track in self.dataset[artist_key]['tracks']:
                if self.name.lower() in track['title'].lower():
                    msg = f'''#### **{track["title"]}**
                                - Artist: {artist_key}
                                - Features: {track["features"]}
                                - Misc: {track["misc"]}
                                - YouTube ID: {track["youtube_id"]}
                                - File Type: {track["filetype"]}\n'''
                    artists_list.append(msg)

        return f"# Database: {self.filename}\n\n" + f"## Tracks with name matching '{self.name}':\n" + "\n".join(artists_list)
