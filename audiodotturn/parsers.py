import argparse
from audiodotturn.config import defaults

class Parser:
    """
    A parser to handle command-line arguments for the AudioDotTurn application.
    """
    def __init__(self):
        """
        Initializes the parser with arguments and sub-commands.

        Returns:
            None
        """
        self.parsers = tuple[argparse.ArgumentParser, ...]
        self.parser = argparse.ArgumentParser(description='Format, orgranize and retrieve data from files in an audio library.')
        self.parser.add_argument('--defaults', nargs='?', choices = ['program', 'format', 'options', 'all'], const='all', help='Show default settings')
        self.parser.add_argument('-v', '--version', action='store_true', help='Show current version of audiodotturn')
        self.subparsers = self.parser.add_subparsers(dest='command')
        self.set_parser = self.subparsers.add_parser('set', help='Set defaults')
        self.settings_list = [
            {
                "name": "artist",
                "description": "default artist name for audio files"
            },
            {
                "name": "title",
                "description": "default title for audio files"
            },
            {
                "name": "features",
                "description": "default features for audio files"
            },
            {
                "name": "misc",
                "description": "default miscellaneous info for audio files"
            },
            {
                "name": "youtube_id",
                "description": "default YouTube ID for audio files"
            },
            {
                "name": "filetype",
                "description": "default audio file type"
            },
            {
                "name": "dry_set",
                "description": "default dry run setting"
            },
            {
                "name": "filename",
                "description": "default json filename"
            },
            {
                "name": "directory",
                "description": "default working directory"
            },
            {
                "name": "formatter",
                "description": "default formatter"
            },
            {
                "name": "error_msg",
                "description": "default error message"
            },
            {
                "name": "exts",
                "description": "default formattable file extensions"
            }
        ]

        for setting in self.settings_list:
            self.set_parser.add_argument(f"--{setting['name']}", dest=setting['name'], type=str, help=setting['description'])
        self.set_parser.add_argument("--dry", "--dry_run", action='store_true', help='Dry run')

        self.create_parser = self.subparsers.add_parser('create', help='Create subcommands')
        self.create_parser.add_argument('-d', '--dirs', action='store_true', help='Organize files in artist directories')
        self.create_parser.add_argument('-f', '--formatfile', type=str, help='Format single file')
        self.create_parser.add_argument('-x', '--formatter', type=str, default=defaults.formatter, help='Define the formatter to use.')
        self.create_parser.add_argument('-F', '--formatdir', action='store_true', help='Format all files in directory')
        self.create_parser.add_argument('-D', '--dump', action='store_true', help='Dump directory into JSON file')
        self.create_parser.add_argument('--filename', type=str, default=defaults.filename, help='Name of JSON file')
        self.create_parser.add_argument('--dry', action='store_true', help='Dry run')
        self.create_parser.add_argument('--directory', type=str, default=defaults.directory, help='Directory to organize or format files')

        self.view_parser = self.subparsers.add_parser('view', help='View subcommands')
        self.view_parser.add_argument('-d', '--data', type=str, help='JSON data to view')
        self.view_subparsers = self.view_parser.add_subparsers(dest='view_command')

        # Create parser for the "artists" subcommand of the "view" command
        self.artists_parser = self.view_subparsers.add_parser('artists', help='View list of artists')
        self.artists_parser.add_argument('-t', '--tracks', action='store_true', help='View list of artists and their tracks')
        self.artists_parser.add_argument('-n', '--names', action='store_true', help='View list of artist names')

        self.songs_parser = self.view_subparsers.add_parser('songs', help='View list of songs')
        self.songs_parser.add_argument('-a', '--artist', type=str, help='View list of songs by artist')
        self.songs_parser.add_argument('-i', '--id', type=str, help='View list of songs by ID')
        self.songs_parser.add_argument('-N', '--name', type=str, help='View list of songs by name')


    def get_parsers(self):
        """
        Return a tuple of parsers that can be used to parse command-line arguments.

        Returns:
            tuple: A tuple of parsers that can be used to parse command-line arguments.
        """
        self.parsers = (self.parser, self.create_parser, self.view_parser)
        return self.parsers
    
    def parse_args(self, args=None):
        """
        Parse command-line arguments using the parser.

        Args:
            args (list): The arguments to parse. If None, command-line arguments are used.

        Returns:
            Namespace: argparse.Namespace object of the parsed arguments.
        """
        return self.parser.parse_args(args)
