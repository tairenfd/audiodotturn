"""
parsers.py
----------

Classes
-------
- `Parser`

Notes
-----
None.
"""
import argparse

class Parser:
    """
    A parser to handle command-line arguments for AudioDotTurn.

    Attributes:
        parser (argparse.ArgumentParser): The top-level parser.
        subparsers (argparse._SubParsersAction): The subparsers for the "set", "create", and "view" commands.
        set_parser (argparse.ArgumentParser): The parser for the "set" command.
        formatting_group (argparse._ArgumentGroup): The formatting options for the "set" command.
        program_group (argparse._ArgumentGroup): The program options for the "set" command.
        create_parser (argparse.ArgumentParser): The parser for the "create" command.
        view_parser (argparse.ArgumentParser): The parser for the "view" command.
        view_subparsers (argparse._SubParsersAction): The subparsers for the "artists" and "songs" subcommands of the "view" command.
        artists_parser (argparse.ArgumentParser): The parser for the "artists" subcommand of the "view" command.
        songs_parser (argparse.ArgumentParser): The parser for the "songs" subcommand of the "view" command.
        parsers (tuple): A tuple of parsers that can be used to parse command-line arguments.

    Methods:
        __init__(): Initializes the parser with arguments and sub-commands.
        get_parsers(): Returns a tuple of parsers that can be used to parse command-line arguments.
        parse_args(args=None): Parse command-line arguments using the parser.
    """
    def __init__(self):
        """
        Initializes the parser with arguments and sub-commands.

        Returns:
            None
        """
        self.parser = argparse.ArgumentParser(description='Format, organize and retrieve data from audio files.')
        
        # Add top-level arguments
        self.parser.add_argument('-v', '--version', action='store_true', help='Show current version of audiodotturn')
        self.parser.add_argument('-c', '--config', help='Path to a specific configuration file to use for the session.')
        self.parser.add_argument('-D', '--database', help='Path to .db file for library database')
        self.parser.add_argument('--defaults', nargs='?', choices=['program', 'format', 'all'], const='all', help='Show default settings')
        self.parser.add_argument('--options', nargs='?', choices=['program', 'format', 'all'], const='all', help='Show default settings')
        
        # Add subparsers for "set", "create", and "view" commands
        self.subparsers = self.parser.add_subparsers(dest='command')
        
        # Create parser for the "set" command
        self.set_parser = self.subparsers.add_parser('set', help='Set defaults')
        self.set_parser.add_argument('-d', '--dry', action='store_true', help='Dry run')
        self.formatting_group = self.set_parser.add_argument_group('formatting options')
        self.formatting_group.add_argument('-a', '--artist', help='Default artist name for audio files')
        self.formatting_group.add_argument('-t', '--title', help='Default title for audio files')
        self.formatting_group.add_argument('-f', '--features', help='Default features for audio files')
        self.formatting_group.add_argument('-m', '--misc', help='Default miscellaneous info for audio files')
        self.formatting_group.add_argument('-y', '--youtube-id', help='Default YouTube ID for audio files')
        self.formatting_group.add_argument('--filetype', help='Default audio file type')
        self.program_group = self.set_parser.add_argument_group('program options')
        self.program_group.add_argument('-s', '--dryset', choices=["true", "false"], help='Default dry run setting')
        self.program_group.add_argument('-q', '--data', help='Default JSON filename')
        self.program_group.add_argument('-p', '--path', dest='directory', help='Default working directory')
        self.program_group.add_argument('-x', '--extractor', choices=["default", "standard", "normal", "yt", "youtube"], help='Default extractor')
        self.program_group.add_argument('-b', '--constructor', help='Default constructor')
        self.program_group.add_argument('-e', '--error', dest='errormsg', help='Default error message options. comma seperated string of options.')
        self.program_group.add_argument('--exts', help='Default formattable file extensions. comma seperated string of options.')
        
        # Create parser for the "create" command
        self.create_parser = self.subparsers.add_parser('create', help='Create subcommands')
        self.create_parser.add_argument('-f', '--format', help='Format single file')
        self.create_parser.add_argument('-x', '--extractor', help='Define the extractor to use')
        self.create_parser.add_argument('-b', '--constructor', help='Define the constructor to use')
        self.create_parser.add_argument('-F', '--formatdir', action='store_true', help='Format all files in directory')
        self.create_parser.add_argument('-o', '--organize', action='store_true', help='Organize all files in directory and create database entries if they dont exist.')
        self.create_parser.add_argument('--dry', action='store_true', help='Dry run')
        self.create_parser.add_argument('-p', '--path', dest='directory', help='Directory to organize or format files, the programs working directory')
        
        # Create parser for the "view" command
        self.view_parser = self.subparsers.add_parser('view', help='View subcommands')
        self.view_subparsers = self.view_parser.add_subparsers(dest='view_command')
        
        # Create parser for the "artists" subcommand of the "view" command
        self.artists_parser = self.view_subparsers.add_parser('artists', help='View list of artists')
        self.artists_parser.add_argument('-T', '--tracks', action='store_true', help='View list of artists and their tracks')
        self.artists_parser.add_argument('-N', '--names', action='store_true', help='View list of artist names')

        # Create parser for the "songs" subcommand of the "view" command
        self.songs_parser = self.view_subparsers.add_parser('songs', help='View list of songs')
        self.songs_parser.add_argument('-A', '--artist', help='View list of songs by artist')
        self.songs_parser.add_argument('-I', '--id', help='View list of songs by ID')
        self.songs_parser.add_argument('-N', '--name', help='View list of songs by track name')
        self.songs_parser.add_argument('-T', '--filetype', help='View list of songs by filetype')
        self.songs_parser.add_argument('-L', '--features', help='View list of songs by included features')
        self.songs_parser.add_argument('-M', '--misc', help='View list of songs by included features')

        self.parsers = (self.parser,) # Set parsers to tuple containing the top-level parser

    def get_parsers(self):
        """
        Return a tuple of parsers that can be used to parse command-line arguments.
            parser, create_parser, view_parser, set_parser
        Returns:
            tuple: A tuple of parsers that can be used to parse command-line arguments.
        """
        self.parsers = (self.parser, self.create_parser, self.view_parser, self.set_parser)
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
