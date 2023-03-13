import argparse

class Parser:
    def __init__(self):
        """
        Initializes the parser with arguments and sub-commands.

        Returns:
            None
        """
        self.parser = argparse.ArgumentParser(description='Format, organize and retrieve data from audio files.')
        
        # Add top-level arguments
        self.parser.add_argument('-v', '--version', action='store_true', help='Show current version of audiodotturn')
        self.parser.add_argument('-p', '--cfgpath', help='Path to a specific configuration file to use for the session.')
        self.parser.add_argument('-d', '--dbpath', help='Path to .db file for library database')
        self.parser.add_argument('-s', '--settings', action='store_true', help='Show current settings')
        
        # Add subparsers
        self.subparsers = self.parser.add_subparsers(dest='command')
        
        # Create parser for the "extract" command
        self.extract_parser = self.subparsers.add_parser('extract', help='Extraction commands')
        self.extract_parser.add_argument('-o', '--out', default="dict",type=str, help='Output format for extraction, default is dict.')
        self.extract_parser.add_argument('-f', '--file', type=str, help='Extract info from single file.')
        self.extract_parser.add_argument('-m', '--multi', nargs="+", type=str, help='Extract info from multiple files.')
        self.extract_parser.add_argument('-l', '--dir', type=str, help='Extract info from files in a directory.')
        
        # Create parser for the "construct" command
        self.construct_parser = self.subparsers.add_parser('construct', help='Construction commands')
        self.construct_parser.add_argument('-a', '--auto', action="store_true", help='Set auto-choice')
        self.construct_parser.add_argument('-c', '--constructor', default="simple", help='Constructor to use')
        self.construct_parser.add_argument('-f', '--file', help='Construct from a single file')
        self.construct_parser.add_argument('-m', '--multi', nargs="+", help='Construct from multiple files')

        # Create parser for the "database" commands
        self.database_parser = self.subparsers.add_parser('database', help='Database commands')
        self.database_parser.add_argument('-f', '--updatefile', help="Update database via file.")
        self.database_parser.add_argument('-m', '--updatemulti', nargs="+", help="Update database via multiple files.")
        self.database_parser.add_argument('-A', '--artists', action="store_true", help='View all artists within the database')
        self.database_parser.add_argument('-S', '--songs', action="store_true", help='View all songs by each artist within the database')
        self.database_parser.add_argument('-Ai', '--artistid', type=int, help='View songs by artist id')
        self.database_parser.add_argument('-Si', '--songid', type=int, help='View song by song id')

    def get_parsers(self):
        """
        Return a list of parsers that can be used to parse command-line arguments.
            parser, create_parser, view_parser, set_parser
        """
        parsers = [self.parser, self.extract_parser, self.construct_parser, self.database_parser]
        return parsers
    
    def parse_args(self, args=None):
        """
        Parse command-line arguments using the parser.

        Args:
            args (list): The arguments to parse. If None, command-line arguments are used.

        Returns:
            Namespace: argparse.Namespace object of the parsed arguments.
        """
        return self.parser.parse_args(args)