import argparse
from config import Config

defaults = Config()

# Create main parser
parser = argparse.ArgumentParser(description='Format, orgranize and retrieve data from files in an audio library.')
parser.add_argument('--defaults', action='store_true', help='Show default settings')

# Create subparsers
subparsers = parser.add_subparsers(dest='command')

# Create parser for the "create" command
create_parser = subparsers.add_parser('create', help='Create subcommands')
create_parser.add_argument('-d', '--dirs', action='store_true', help='Organize files in artist directories')
create_parser.add_argument('-f', '--formatfile', type=str, help='Format single file')
create_parser.add_argument('-F', '--formatdir', action='store_true', help='Format all files in directory')
create_parser.add_argument('-D', '--dump', action='store_true', help='Dump directory into JSON file')
create_parser.add_argument('--filename', type=str, default=defaults.filename, help='Name of JSON file')
create_parser.add_argument('--dry', action='store_true', help='Dry run')
create_parser.add_argument('--directory', type=str, default=defaults.directory, help='Directory to organize or format files')

# Create parser for the "view" command
view_parser = subparsers.add_parser('view', help='View subcommands')
view_parser.add_argument('-d', '--data', type=str, help='JSON data to view')
view_subparsers = view_parser.add_subparsers(dest='view_command')

# Create parser for the "artists" subcommand of the "view" command
artists_parser = view_subparsers.add_parser('artists', help='View list of artists')
artists_parser.add_argument('-t', '--tracks', action='store_true', default='False', help='View list of artists and their tracks')
artists_parser.add_argument('-n', '--names', action='store_true', default='False', help='View list of artist names')

# Create parser for the "songs" subcommand of the "view" command
songs_parser = view_subparsers.add_parser('songs', help='View list of songs')
songs_parser.add_argument('-a', '--artist', type=str, help='View list of songs by artist')
songs_parser.add_argument('-i', '--id', type=str, help='View list of songs by ID')
songs_parser.add_argument('-N', '--name', type=str, help='View list of songs by name')

# Parse arguments
args = parser.parse_args()

parsers = (parser, create_parser, view_parser)
