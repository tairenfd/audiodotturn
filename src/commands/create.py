import os
import re
import json
import shutil
import argparse
from rich.markdown import Markdown
from config import Config


class Create(Config):
    def __init__(self, args: argparse.Namespace):
        self.args = args
        super().__init__()
        self.dry = args.dry
        self.filename = self.args.filename
        self.directory = self.args.directory

    def run(self):
        if self.args.dirs:
            self.msg = self.dirs()
        elif self.args.formatfile:
            self.filename = self.args.formatfile
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
