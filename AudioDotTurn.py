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


class Settings:
    def __init__(self,
                 dataset: dict = None,
                 filename: str = 'data.json',
                 directory: str = '.',
                 dry: bool = False,
                 artist: str = "UKNOWN",
                 title: str = "UKNOWN",
                 features: str = "UKNOWN",
                 misc: str = "UKNOWN",
                 youtube_id: str = "UKNOWN",
                 filetype: str = "mp3",
                 dump: dict = {}
        ):
        self.dataset = dataset
        self.filename = filename
        self.dry = dry
        self.directory = directory
        self.artist = artist
        self.title = title
        self.features = features
        self.misc = misc
        self.youtube_id = youtube_id
        self.filetype = filetype
        self.msg = ''
        self.dump = dump
        self.console = Console()

class Create(Settings):
    def __init__(self, args):
        self.args = args
        super().__init__(filename=args.filename,
                         dry=args.dry,
                         directory=args.directory
                        )

    def run(self):
        if self.args.dirs:
            self.msg = self.dirs()
        elif self.args.formatfile:
            self.msg = f'### **{self.format_file()}**'
        elif self.args.formatdir:
            self.msg = self.format_files_dir()
        elif self.args.create_command == 'json':
            if self.args.dump:
                self.msg = (self.json_dump())
        return self.console.print(Markdown(self.msg))

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
                formatted.append(f'    - {file}')
        stats = [
            f'\n### Number of files formatted: {len(formatted) - 1}',
            f'\n### Number of files unable to be formatted: {len(not_formatted) - 1}',
            f'\n### Number of files unchanged: {len(already_formatted) - 1}'
        ]

        return formatted, not_formatted, already_formatted, stats

    def dirs(self):
        directory = self.directory.rstrip('/')
        artists, files = set(), set()
        created = []
        exts = (
            '.mp3',
            '.mp4',
            '.wav',
            '.m4a',
            '.wma',
            '.aac',
            '.flac',
            '.webm',
            '.ogg',
            '.opus',
            '.flv'
        )
        for filename in os.listdir(self.directory):
            if filename.endswith(exts):
                match = re.match(r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", filename)
                if match:
                    self.artist = match.group(1)
                files.add(self.artist)
                artist_dir = f"{directory}/{self.artist.title()}"
                if not os.path.exists(artist_dir):
                    artists.add(self.artist)
                    if not self.dry:
                        os.makedirs(artist_dir)
                    created.append(f'                    -{artist_dir}/')
                if not self.dry:
                    try:
                        shutil.move(f"{self.directory}/{filename}", f"{artist_dir}/{filename}")
                    except:
                        pass
        return f'### Organized {len(files)} files for {len(artists)} artists.\n' + '#### Created directories:\n' + '\n'.join(created)

    def format_files_dir(self):
        directory = self.directory.rstrip('/')
        try:
            files_list = [self.format_file(file=f) for f in os.listdir(directory) if os.path.isfile(directory+'/'+f)]
            formatted, not_formatted, already_formatted, stats = self.form_or_not(files_list)
            return '\n'.join(formatted + not_formatted + already_formatted + stats)
        except Exception as error:
            return f'{error}'

    def format_file(self, file: str = None):
        # Extract information from filename
        # pattern = r'^(.+?) - (.+?)(?: \((feat\. .+?)\))? (\[.+?\])?\.mp3$'
        if file:
            self.filename = file
        file = self.filename
        format_check = re.search(r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file)
        if format_check:
            return '$$'+self.filename

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
            return f"*****{self.filename}"

        else:
            if match_features:
                self.features = ''
                self.features += match_features.group(2) if match_features.group(2) else ''
                self.features += match_features.group(4) if match_features.group(4) else ''
                self.features += match_features.group(6) if match_features.group(6) else ''
                features = self.features.strip()

            features = self.features
            misc = ', '.join(match_misc).strip('()') if match_misc else self.misc
            
            if not match.group(5):
                artist = match.group(1).strip() if match.group(1) else self.artist
                youtube_id = match.group(3).strip('[]') if match.group(3) else self.youtube_id
                filetype = match.group(4).strip().rstrip('.') if match.group(4) else self.filetype
            else:
                artist = match.group(5).strip() if match.group(5) else self.artist
                youtube_id = match.group(6).strip('[]') if match.group(6) else self.youtube_id
                filetype = match.group(7).strip().rstrip('.') if match.group(7) else self.filetype

            title = match.group(2).strip() if match.group(2) else self.title
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
            if self.filename != new_file and not self.dry:
                os.rename(self.directory+'/'+self.filename, self.directory+'/'+new_file)

            return new_file

    def json_dump(self):
        if not os.path.isdir(self.directory):
            return Markdown('### **Directory path not found.**')

        data = {}
        for root, _, files in os.walk(self.directory):
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
                    "youtube_id": youtube_id,
                    "filetype": filetype
                })

        if not self.dry:
            with open(os.path.join(self.filename), 'w') as f:
                json.dump(data, f, indent=2)
            return Markdown(f"### **Data has been dumped into {self.filename}.**")        

        return Markdown(data)


# View Commands
class View(Settings):
    def __init__(self, args: argparse.Namespace):
        self.args = args
        try:
            with open(os.path.join(self.args.data), 'r') as f:
                self._dataset = json.load(f, object_hook=dict)
        except Exception as error:
            self._dataset = {}
            self.args.view_command = f'{error}'

        super().__init__(dataset=self._dataset)

    def run(self):
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

        self.console.print(Markdown(self.msg))

    # View - artists commands
    def get_artists(self):
        # get list of all artists in dataset
        artists_list = []
        for artist in self.dataset:
            artists_list.append(f'                            - {artist}')

        return f"# Database: {self.filename}\n\n" + "## Artists:\n" + '\n'.join(artists_list)

    def get_artists_tracks(self):
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
    def get_songs_by_artist(self):
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

    def get_songs_by_id(self):
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

    def get_songs_by_name(self):
    # get list of all songs by their name in dataset, will search by substring
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

class AudioDotTurn:
    def __init__(self, args: argparse.Namespace, parsers: tuple((argparse.ArgumentParser, ...))):
        self.args = args
        self.parser = parsers[0]
        self.create_parser = parsers[1]
        self.view_parser = parsers[2]

        if self.args.command == 'create':
            creator = Create(self.args)
            if not any((self.args.dirs, self.args.formatfile, self.args.formatdir)):
                self.create_parser.print_help()
                exit(1)
            creator.run()

        elif args.command == 'view':
            viewer = View(self.args)
            if not self.args.data:
                self.view_parser.print_help()
                exit(1)
            if any(args.view_command):
                viewer.run()


        else:
            self.parser.print_help()

def main():

    # Create main parser
    parser = argparse.ArgumentParser(description='Format, orgranize and retrieve data from files in an audio library.')

    # Create subparsers
    subparsers = parser.add_subparsers(dest='command')

    # Create parser for the "create" command
    create_parser = subparsers.add_parser('create', help='Create subcommands')
    create_parser.add_argument('-d', '--dirs', action='store_true', help='Organize files in artist directories')
    create_parser.add_argument('-f', '--formatfile', action='store_true', help='Format single file')
    create_parser.add_argument('-F', '--formatdir', action='store_true', help='Format all files in directory')
    create_parser.add_argument('-D', '--dump', action='store_true', help='Dump directory into JSON file')
    create_parser.add_argument('--filename', type=str, default='data.json', help='Name of JSON file')
    create_parser.add_argument('--dry', action='store_true', help='Dry run')
    create_parser.add_argument('--directory', type=str, default='.', help='Directory to organize or format files')

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

    # Initiate tool
    tool = AudioDotTurn(args=args, parsers=parsers)

if __name__ == "__main__":
    main()
