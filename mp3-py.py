import os
import re
import json
import argparse
import shutil
from rich import print
from rich.pretty import pprint
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

class MP3Create:
        def __init__(self, filename: str = 'data.json'):
            self.filename = filename

        def form_or_not(self, files_list: list):
            formatted = ['\n## Formatted:']
            not_formatted = ['\n## Not Formatted:']
            already_formatted = ['\n## No Change:']
            for file in files_list:
                if file.startswith('*****'):
                    not_formatted.append(f"    - {file.lstrip('*')}")
                elif file.startswith('$$'):
                    already_formatted.append(f"    - {file.lstrip('$$')}")
                else:
                    formatted.append(f'- {file}')
            stats = [
                f'\n### Number of files formatted: {len(formatted) - 1}',
                f'\n### Number of files unable to be formatted: {len(not_formatted) - 1}',
                f'\n### Number of files unchanged: {len(already_formatted) - 1}'
            ]

            return formatted, not_formatted, already_formatted, stats

        def dirs(self, directory):
            directory = directory.rstrip('/')
            artists = set()
            files = set()
            created = []
            for filename in os.listdir(directory):
                match = re.match(r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", filename)
                if match:
                    artist = match.group(1)
                else:
                    artist = "UNKNOWN"
                files.add(artist)
                artist_dir = f"{directory}/{artist.title()}"
                if not os.path.exists(artist_dir):
                    artists.add(artist)
                    os.makedirs(artist_dir)
                    created.append(f'                    -{artist_dir}/')
                try:
                    shutil.move(f"{directory}/{filename}", f"{artist_dir}/{filename}")
                except:
                    pass
            msg = f'### Organized {len(files)} files for {len(artists)} artists.\n' + '#### Created directories:\n' + '\n'.join(created)
            return Markdown(msg)
    
        def format_files_dir(self, directory):
            directory = directory.rstrip('/')
            try:
                files_list = [self.format_file(file=f, directory=directory) for f in os.listdir(directory) if os.path.isfile(directory+'/'+f)]
                formatted, not_formatted, already_formatted, stats = self.form_or_not(files_list)
                return Markdown('\n'.join(formatted + not_formatted + already_formatted + stats))
            except Exception as error:
                return Markdown(f'{error}')

        def format_file(self, file: str = None, directory: str = '.'):
            # Extract information from filename
            # pattern = r'^(.+?) - (.+?)(?: \((feat\. .+?)\))? (\[.+?\])?\.mp3$'
            _file = file
            format_check = re.search(r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file)
            if format_check:
                return '$$'+_file

            match_features = re.search(r'([fF]t\. |[wW]\/)(.+?)(?=([\'\"\"\"]|[(]|[-]|[\[]))|\([fF]eat\. (.+?)\)|([fF]eat\. (.+?)(?=([\'\"\"\"]|[(]|[-]|[\[])))', file)
            if match_features:
                file = file.replace(match_features[0].rstrip('-(['), '')

            match_misc_1 = re.findall(r'\(.+?\)', file)
            match_misc_2 = re.findall(r'(\[.+?\]) +?', file)
            match_misc = match_misc_1 + match_misc_2

            if match_misc:
                for match in match_misc:
                    file = file.replace(match, '').replace('  ', ' ')
                    match_misc[match_misc.index(match)] = match.strip('()[] ')
            match = re.search(r'^(.+?)-(.+?) (\[\S+\])?\.(.*$)|^(.+) (\[\S+\])?\.(.*$)', file)

            if not match:
                match = re.search(r'(.+?).([\"\uFF02\'].+?[\"\uFF02\']).(\[.+?\])?\.(.*$)', file)

            if not match:
                return f"*****{_file}"

            else:
                artist, title, features, misc, youtube_id, filetype = 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', 'mp3'
                if match_features:
                    features = ''
                    features += match_features.group(2) if match_features.group(2) else ''
                    features += match_features.group(4) if match_features.group(4) else ''
                    features += match_features.group(6) if match_features.group(6) else ''

                if features != "UNKNOWN":
                    features = features.strip()

                misc = ', '.join(match_misc).strip('()') if match_misc else misc
                
                if not match.group(5):
                    artist = match.group(1).strip() if match.group(1) else artist
                    youtube_id = match.group(3).strip('[]') if match.group(3) else youtube_id
                    filetype = match.group(4).strip().rstrip('.') if match.group(4) else filetype
                else:
                    artist = match.group(5).strip() if match.group(5) else 'UNKNOWN'
                    youtube_id = match.group(6).strip('[]') if match.group(6) else youtube_id
                    filetype = match.group(7).strip().rstrip('.') if match.group(7) else filetype

                title = match.group(2).strip() if match.group(2) else title
                title_in_artist = re.search(r'([\uFF02\"\'].+?[\uFF02\"\'])|(:.+)', artist)
                if title_in_artist and title == "UNKNOWN":
                    if title_in_artist.group(1):
                        artist = artist.replace(title_in_artist.group(1), '').strip()
                        title = title_in_artist.group(1)
                    else:
                        artist = artist.replace(title_in_artist.group(2), '').strip()
                        title = title_in_artist.group(2)
                    # title = title.replace('\uFF02', '')
                    title = title.strip('":\uFF02\'')
                    title = title.strip()

                new_file = f"[{artist}][{title}][{features}][{misc}][{youtube_id}].{filetype}"
                if _file != new_file:
                    os.rename(directory+'/'+_file, directory+'/'+new_file)
                return new_file



class MP3View:
    def __init__(self, dataset: dict = None, filename: str = 'data.json'):
        self.dataset = dataset
        self.filename = filename
        
    def json_dump(self, directory: str):
        if not os.path.isdir(directory):
            return Markdown('### **Directory path not found.**')

        data = {}
        for root, _, files in os.walk(directory):
            for file in files:
                # Parse filename using regular expressions
                match = re.match(r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file)
                if match:
                    artist, title, features, misc, youtube_id, filetype = match.groups()
                else:
                    continue

                # Add track data to nested dictionary
                if artist not in data:
                    data[artist] = {"tracks": []}
                data[artist]["tracks"].append({
                    "title": title,
                    "features": features,
                    "misc": misc,
                    "video_id": youtube_id,
                    "filetype": filetype
                })

        with open(os.path.join(directory, self.filename), 'w') as f:
            json.dump(data, f, indent=2)
    
        return Markdown(f"### **Data has been dumped into {self.filename} in {directory}.**")        

    def get_artists(self):
        # get list of all artists (will search by substring) in dataset
        artists_list = []
        for artist in self.dataset:
            artists_list.append(f'                            - {artist}')

        msg = f"# Database: {self.filename}\n\n" + "## Artists:\n" + '\n'.join(artists_list)
        return Markdown(msg)

    def get_artists_tracks(self):
        # get list of all artists (will search by substring) and their tracks in dataset
        artists_list = []
        for artist in self.dataset:
            artists_list.append(f'### Artist: **{artist}**')
            for tracks in self.dataset[artist]['tracks']:
                msg = f'''#### Track: {tracks["title"]}
                            - Artist: {artist}
                            - Features: {tracks["features"]}
                            - Misc: {tracks["misc"]}
                            - YouTube ID: {tracks["video_id"]}
                            - File Type: {tracks["filetype"]}\n'''
                artists_list.append(msg)

        msg = f"# Database: {self.filename}\n\n" + "## Artists and their Tracks:\n" + '\n'.join(artists_list)
        return Markdown(msg)

    def get_songs_by_artist(self, artist: str):
        # get list of all songs by an artist (will search by substring) name in dataset (optional func: get_artists_tracks)
        artists_list = []
        for artist_key in self.dataset.keys():
            if artist.lower() in artist_key.lower():
                for track in self.dataset[artist_key]['tracks']:
                    msg = f'''#### **{track["title"]}**
                                - Artist: {artist_key}
                                - Features: {track["features"]}
                                - Misc: {track["misc"]}
                                - YouTube ID: {track["video_id"]}
                                - File Type: {track["filetype"]}\n'''
                    artists_list.append(msg)

        msg = f"# Database: {self.filename}\n\n" + f"## Songs by artist matching '{artist}':\n" + '\n'.join(artists_list)
        return Markdown(msg)

    def get_songs_by_id(self, id: str):
        # get list of all songs by their youtube id in dataset
        artists_list = []
        for artist_key in self.dataset.keys():
            for track in self.dataset[artist_key]['tracks']:
                if id in track['video_id']:
                    msg = f'''#### **{track["title"]}**
                                - Artist: {artist_key}
                                - Features: {track["features"]}
                                - Misc: {track["misc"]}
                                - YouTube ID: {track["video_id"]}
                                - File Type: {track["filetype"]}\n'''
                    artists_list.append(msg)

        msg = f"# Database: {self.filename}\n\n" + f"## Songs by ID {id}:\n" + '\n'.join(artists_list)
        return Markdown(msg)

    def get_songs_by_name(self, name: str):
    # get list of all songs by their name in dataset, will search by substring
        artists_list = []
        for artist_key in self.dataset.keys():
            for track in self.dataset[artist_key]['tracks']:
                if name.lower() in track['title'].lower():
                    msg = f'''#### **{track["title"]}**
                                - Artist: {artist_key}
                                - Features: {track["features"]}
                                - Misc: {track["misc"]}
                                - YouTube ID: {track["video_id"]}
                                - File Type: {track["filetype"]}\n'''
                    artists_list.append(msg)

        msg = f"# Database: {self.filename}\n\n" + f"## Tracks with name matching '{name}':\n" + "\n".join(artists_list)
        return Markdown(msg)

def main():

    # Create main parser
    parser = argparse.ArgumentParser(description='Create and retrieve data from MP3 dataset. Organize mp3 files.')

    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

    # Create "create" subparser
    create_parser = subparsers.add_parser('create', help='Create artist directories and a JSON dataset of the MP3 files')
    create_parser.add_argument(
        '--dirs', '-d',
        nargs='?',
        type=str,
        const='.',
        metavar='DIRECTORY',
        help='Process formatted MP3 files from --format{file, dir} in DIRECTORY into directories'
    )
    create_parser.add_argument(
        '--formatfile', '-f',
        metavar='FILENAME',
        help='Attempt to format FILENAME into proper filename'
    )

    create_parser.add_argument(
        '--formatdir', '-fd',
        nargs='?',
        type=str,
        const='.',
        metavar='DIRECTORY',
        help='Attempt to format files from DIRECTORY into proper filenames. Default is CWD'
    )

    # Create "view" subparser
    view_parser = subparsers.add_parser('view', help='View MP3 dataset. --data flag reqired for all view commands.')
    view_parser.add_argument(
        '--data',
        required=True,
        type=str,
        metavar='DATASET',
        help='Specify the JSON dataset file to be viewed or altered. IF THIS IS NOT SET VIEW TOOLS CANNOT BE USED'
    )
    view_subparsers = view_parser.add_subparsers(dest='view_command', help='Commands dependent on --data')

    # Create 'json' subparser under 'view'
    json_parser = view_subparsers.add_parser(
       'json',
        help='JSON tools' 
    )
    json_parser.add_argument(
        '--dump', '-D',
        nargs='?',
        metavar='DIRECTORY',
        const='.',
        help='Create a JSON of formatted mp3 files in DIRECTORY. Default directory is cwd. Outfile is DATASET'
    )
    
    # Create "artists" subparser under "view"
    artists_parser = view_subparsers.add_parser(
        'artists',
        help='Artist information'
    )
    artists_parser.add_argument(
        '--tracks',
        action='store_true',
        help='List all artists in the dataset and their tracks'
    )
    artists_parser.add_argument(
        '--names',
        action='store_true',
        help='List all artists in the dataset'
    )

    # Create "songs" subparser under "view"
    songs_parser = view_subparsers.add_parser(
        'songs',
        help='Song information'
    )
    songs_parser.add_argument(
        '--artist', '--by-artist', '-a',
        metavar='ARTIST',
        help='Specify the artist to display songs for'
    )
    songs_parser.add_argument(
        '--id', '--by-id',
        metavar='YOUTUBE_ID',
        help='Search for song by youtube id'
    )
    songs_parser.add_argument(
        '--name', '--by-name', '-n',
        metavar='TRACK_TITLE',
        help='Search for song by track title'
    )

    # Parse arguments
    args = parser.parse_args()

    # Init rich console for markdown and json rendering
    console = Console()

    # Execute commands
    # Create commands
    if args.command == 'create':
        creator = MP3Create()
        if args.dirs:
            console.print(creator.dirs(args.dirs))
        if args.formatfile:
            console.print(Markdown(f'### **{creator.format_file(args.formatfile)}**'))
        if args.formatdir:
            console.print(creator.format_files_dir(args.formatdir))
        if not any((args.dirs, args.formatfile, args.formatdir)):
            create_parser.print_help()

    # View commands
    elif args.command == 'view':
        if not args.data or not any(
            (args.view_command == 'json', args.view_command == 'artists', args.view_command == 'songs')
        ):
            view_parser.print_help()
            exit(1)

        dataset = None

        if os.path.isfile(args.data):
            with open(args.data, 'r') as file:
                dataset = json.load(file)
        elif args.data.endswith('.json'):
            if args.view_command == 'json':
                if args.dump:
                    with open(os.path.join(args.dump, args.data), 'a') as file:
                        file.write('{}')
                else:
                    with open(args.dump, 'a') as file:
                        file.write('{}')
            else:
                console.print(Markdown("### JSON dataset doesn't seem to exist"))
                exit(1)
        else:
            console.print(Markdown('### File must be a JSON'))
            exit(1)

        viewer = MP3View(dataset, filename=args.data)

        if args.view_command == 'json':
            if args.dump:
                console.print(viewer.json_dump(directory=args.dump))
            else:
                json_parser.print_help()
            
        elif args.view_command == 'artists':
            if args.tracks:
                console.print(viewer.get_artists_tracks())
            if args.names:
                console.print(viewer.get_artists())
            if not any((args.tracks, args.names)):
                artists_parser.print_help()

        elif args.view_command == 'songs':
            if args.artist:
                console.print(viewer.get_songs_by_artist(args.artist))
            if args.id:
                console.print(viewer.get_songs_by_id(args.id))
            if args.name:
                console.print(viewer.get_songs_by_name(args.name))
            if not any((args.artist, args.id, args.name)):
                songs_parser.print_help()
                
        else:
            view_parser.print_help()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
