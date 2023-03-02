import os
import re
import json
import shutil
import argparse
from rich.tree import Tree
from rich.json import JSON
from rich.markdown import Markdown
from src.config import Config


class Create(Config):
    def __init__(self, args: argparse.Namespace):
        self.args = args
        # grab defaults
        super().__init__()
        # set user defined values
        self.dry = args.dry
        self.filename = self.args.filename
        self.directory = self.args.directory
        self.formatter = self.args.formatter.lower().strip()

    # create runner
    def run(self) -> None:
        with self.console.status("[bold green]Working...") as status:
            if self.args.dirs:
                self.msg = self.dirs()
            elif self.args.formatfile:
                self.filename = self.args.formatfile
                self.msg = f"### **{self.format_file()}**"
            elif self.args.formatdir:
                self.msg = self.format_files_dir()
            elif self.args.dump:
                tree = Tree('DUMP')
                dump = self.json_dump()
                if type(dump) is tuple:
                    tree.add("[green]Runtime Info").add(JSON(dump[0]), highlight=True)
                    tree.add("[cyan]Data").add(JSON(dump[1]), highlight=True)
                else:
                    tree.add("[red]Runtime Info").add(JSON(dump), highlight=True)
                return self.console.log(tree)

            return self.console.log(Markdown(self.msg))

    # check whether a file is formatted, unable to be formatted, or
    # unchanged due to already being formatted or an incompatible extension
    def form_or_not(self, files_list: list) -> tuple[list[str], list[str], list[str], list[str]]:
        formatted = ["\n## Formatted:"]
        not_formatted = ["\n## Not Formatted:"]
        already_formatted = ["\n## No Change:"]
        for file in files_list:
            if file.startswith("*****"):
                not_formatted.append(f"    - {file.lstrip('*')}")
            elif file.startswith("$$"):
                already_formatted.append(f"    - {file.lstrip('$$')}")
            else:
                formatted.append(f"    - {file}")
        stats = [
            f"\n### Number of files formatted: {len(formatted) - 1}",
            f"\n### Number of files unable to be formatted: {len(not_formatted) - 1}",
            f"\n### Number of files unchanged: {len(already_formatted) - 1}",
        ]

        return formatted, not_formatted, already_formatted, stats

    # create directories based off of unique artists in music library
    def dirs(self) -> str:
        directory = self.directory.rstrip("/")
        artists, files = set(), set()
        created = []

        for filename in os.listdir(self.directory):
            if filename.endswith(self.exts):
                match = re.match(
                    r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", filename
                )
                if not match:
                    match = re.match(
                        r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", filename
                    )
                if match:
                    self.artist = match.group(1)
                files.add(self.artist)
                artist_dir = f"{directory}/{self.artist.title()}"
                if not os.path.exists(artist_dir):
                    artists.add(self.artist)
                    if not self.dry:
                        os.makedirs(artist_dir)
                    created.append(f"                    -{artist_dir}/")
                # if dry run, no files will be moved and no directories created,
                # the user just get the data of what wouldve been changed if applied
                if not self.dry:
                    try:
                        shutil.move(
                            f"{self.directory}/{filename}", f"{artist_dir}/{filename}"
                        )
                    except:
                        pass
        return (
            f"### Organized {len(files)} files for {len(artists)} artists.\n"
            + "#### Created directories:\n"
            + "\n".join(created)
        )

    # Attempt to format all files in a given directory, uses form_or_not for listing data to user, dry run settings are handled for this in format_file
    def format_files_dir(self) -> str:
        directory = self.directory.rstrip("/")
        try:
            # go through all files in given directory and only grab the actual files, not directory names and such
            # attempt to format the files as they are found
            files_list = [
                self.format_file(file=f)
                for f in os.listdir(directory)
                if os.path.isfile(directory + "/" + f)
            ]
            formatted, not_formatted, already_formatted, stats = self.form_or_not(
                files_list
            )
            return "\n".join(formatted + not_formatted + already_formatted + stats)
        except Exception as error:
            return f"{error}"

    # file argument really only used by format_files_dir, otherwise will use self.filename
    def format_file(self, file: str = None) -> str:
        # get filename and create a temp filename
        if file:
            self.filename = file
        file = self.filename

        if self.formatter in ["youtube", "yt"]:
            new_file = self.youtube_formatter(self.filename)
        elif self.formatter in ["standard", "default"]:
            new_file = self.standard_formatter(self.filename)

        # if not a dry-run, set the new file name
        if self.filename != new_file and not self.dry:
            os.rename(
                self.directory + "/" + self.filename, self.directory + "/" + new_file
            )

        return new_file

    def json_dump(self) -> str | tuple[str, str]:

        # check if valid directory
        if not os.path.isdir(self.directory):
            return json.dumps(
                {
                    "Result": {
                        "Dry run": f"{self.dry}",
                        "Status": "FAILED",
                        "Final": f"Data has FAILED to be dumped into {self.filename}.",
                        "Reason": f"Directory path '{self.directory}' not found.",
                    }
                }
            )

        # init empty dataset
        data = {}
        for root, _, files in os.walk(self.directory):
            for file in files:
                # Parse filename using regular expressions, if formatted then grab info to add to dataset
                match = re.match(
                    r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file
                )
                if match:
                    artist, title, features, misc, youtube_id, filetype = match.groups()
                else:
                    match = re.match(
                        r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file
                    )
                    if match:
                        artist, title, features, misc, filetype = match.groups()
                        youtube_id = None

                if match:
                    # Add track data to nested dictionary
                    if artist not in data:
                        data[artist] = {"tracks": []}

                    if youtube_id:
                        data[artist]["tracks"].append(
                            {
                                "title": title,
                                "features": features,
                                "misc": misc,
                                "youtube_id": youtube_id,
                                "filetype": filetype,
                            }
                        )

                    else:
                        data[artist]["tracks"].append(
                            {
                                "title": title,
                                "features": features,
                                "misc": misc,
                                "filetype": filetype,
                            }
                        )

        if not data:
            return json.dumps(
                {
                    "Result": {
                        "Dry run": f"{self.dry}",
                        "Status": "FAILED",
                        "Final": f"Data has FAILED to be dumped into {self.filename}.",
                        "Reason": "No data available. Most likely cause is having no formatted files available in directory.",
                    }
                }
            )

        # if not a dry run then create the json dump in the given location
        # otherwise just print it
        if not self.dry:
            with open(os.path.join(self.filename), "w") as f:
                json.dump(data, f, indent=2)
            return json.dumps(
                {
                    "Result": {
                        "Dry run": f"{self.dry}",
                        "Status": "SUCCESS",
                        "Final": f"Data has been dumped into '{self.filename}'.",
                    }
                }
            )

        # return json.dumps(data, indent=2)
        return json.dumps(
            {
                "Result": {
                    "Dry run": f"{self.dry}",
                    "Status": "SUCCESS",
                    "Final": f"Data would have been dumped into '{self.filename}'.",
                }
            }
        ), json.dumps(data)

    # FORMATTERS

    def youtube_formatter(self, file: str) -> str:
        # check if already formatted or if not an audio file, if so add $$ to temp name
        format_check = re.search(
            r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file
        )
        if format_check or not file.endswith(self.exts):
            return "$$" + file

        # check for track features
        features_1 = re.search(r"\([fF]t[\. | ](.+?)\)", file)
        if features_1:
            file = file.replace(features_1[0], "")

        features_2 = re.search(
            r"([fF]t[\. | ]|[wW]\/)(.+?)(?=([\'\"\.]|[()]|[-]|[\[]))", file
        )
        if features_2:
            file = file.replace(features_2[0].rstrip("-[("), "")

        features_3 = re.search(r"\([fF]eat[\. | ](.+?)\)", file)
        if features_3:
            file = file.replace(features_3[0], "")

        features_4 = re.search(
            r"([fF]eat[\. | ](.+?)(?=([\'\"\.]|[()]|[-]|[\[])))", file
        )
        if features_4:
            file = file.replace(features_4[0].rstrip("-["), "")

        features = [features_1, features_2, features_3, features_4]

        # check for misc info
        match_misc_1 = re.findall(r"\(.+?\)", file)
        match_misc_2 = re.findall(r"(\[.+?\](?!\.))[ +?]", file)
        match_misc = match_misc_1 + match_misc_2

        if match_misc:
            for match in match_misc:
                file = file.replace(match, "").replace("  ", " ")
                match_misc[match_misc.index(match)] = match.strip("()[] ")

        # check for rest of values, first for a artist-title combo and then just for artist
        match = re.search(
            r"^(.+?)-(.+?) (\[\S+\])?\.(.*$)|^(.+) (\[\S+\])?\.(.*$)", file
        )

        # at this point if file cant be formatted, add ***** to temp name and move on
        if not match:
            file = self.filename
            return f"*****{file}"

        # if file is formattable, check for existing data and fill it in. Use defaults set in config
        # for cases where no info is available.
        else:
            if any(features):
                self.features = []
                self.features.append(
                    features_1.group(1).strip()
                ) if features_1 else None
                self.features.append(
                    features_2.group(2).strip()
                ) if features_2 else None
                self.features.append(
                    features_3.group(1).strip()
                ) if features_3 else None
                self.features.append(
                    features_4.group(2).strip()
                ) if features_4 else None
                self.features = ", ".join(self.features).replace("'", "")

            features = self.features
            misc = ", ".join(match_misc).strip("()") if match_misc else self.misc

            if not match.group(5):
                artist = match.group(1).strip() if match.group(1) else self.artist
                youtube_id = (
                    match.group(3).strip("[]") if match.group(3) else self.youtube_id
                )
                filetype = (
                    match.group(4).strip().rstrip(".")
                    if match.group(4)
                    else self.filetype
                )
            else:
                artist = match.group(5).strip() if match.group(5) else self.artist
                youtube_id = (
                    match.group(6).strip("[]") if match.group(6) else self.youtube_id
                )
                filetype = (
                    match.group(7).strip().rstrip(".")
                    if match.group(7)
                    else self.filetype
                )

            # if there is no title, double check the artist name to see if its possibly located there
            title = match.group(2).strip() if match.group(2) else self.title
            title_in_artist = re.search(r"([\uFF02\"\'].+?[\uFF02\"\'])|(:.+)", artist)
            if title_in_artist and title == "UNKNOWN":
                if title_in_artist.group(1):
                    artist = artist.replace(title_in_artist.group(1), "").strip()
                    title = title_in_artist.group(1)
                else:
                    artist = artist.replace(title_in_artist.group(2), "").strip()
                    title = title_in_artist.group(2)
                title = title.strip("\":\uFF02'")
                title = title.strip()

            # create formatted file name
            return f"[{artist}][{title}][{features}][{misc}][{youtube_id}].{filetype}"

    def standard_formatter(self, file: str) -> str:
        # check if already formatted or if not an audio file, if so add $$ to temp name
        format_check = re.search(r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file)
        format_check_extra = re.search(
            r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(.+?)$", file
        )
        if format_check or format_check_extra or not file.endswith(self.exts):
            return "$$" + file

        # check for track features

        features_1 = re.search(r"\([fF]t[\. | ](.+?)\)", file)
        if features_1:
            file = file.replace(features_1[0], "")

        features_2 = re.search(
            r"([fF]t[\. | ]|[wW]\/)(.+?)(?=([\'\"\.]|[()]|[-]|[\[]))", file
        )
        if features_2:
            file = file.replace(features_2[0].rstrip("-[("), "")

        features_3 = re.search(r"\([fF]eat[\. | ](.+?)\)", file)
        if features_3:
            file = file.replace(features_3[0], "")

        features_4 = re.search(
            r"([fF]eat[\. | ](.+?)(?=([\'\"\.]|[()]|[-]|[\[])))", file
        )
        if features_4:
            file = file.replace(features_4[0].rstrip("-["), "")

        features = [features_1, features_2, features_3, features_4]

        # check for misc info
        match_misc_search = re.findall(r"(\(.+?\))|(\[.+?\])", file)
        match_misc = []

        if match_misc_search:
            for match in match_misc_search:
                match = match[0] if match[0] else match[1]
                file = file.replace(match, "").replace("  ", " ")
                match_misc.append(match.strip("()[] "))

        # check for rest of values, first for a artist-title combo and then just for artist
        match = re.search(r"^(.+?)-(.+?)\.(.*$)|^(.+)\.(.*$)", file)

        # at this point if file cant be formatted, add ***** to temp name and move on
        if not match:
            file = self.filename
            return f"*****{file}"

        # if file is formattable, check for existing data and fill it in. Use defaults set in config
        # for cases where no info is available.
        else:
            if any(features):
                self.features = []
                self.features.append(
                    features_1.group(1).strip()
                ) if features_1 else None
                self.features.append(
                    features_2.group(2).strip()
                ) if features_2 else None
                self.features.append(
                    features_3.group(1).strip()
                ) if features_3 else None
                self.features.append(
                    features_4.group(2).strip()
                ) if features_4 else None
                self.features = ", ".join(self.features).replace("'", "")

            features = self.features

            misc = ", ".join(match_misc).strip("()") if match_misc else self.misc

            if not match.group(5):
                artist = match.group(1).strip() if match.group(1) else self.artist
                filetype = (
                    match.group(3).strip().rstrip(".")
                    if match.group(3)
                    else self.filetype
                )
            else:
                artist = match.group(4).strip() if match.group(4) else self.artist
                filetype = (
                    match.group(5).strip().rstrip(".")
                    if match.group(5)
                    else self.filetype
                )

            # if there is no title, double check the artist name to see if its possibly located there
            title = match.group(2).strip() if match.group(2) else self.title
            title_in_artist = re.search(r"([\uFF02\"\'].+?[\uFF02\"\'])|(:.+)", artist)
            if title_in_artist and title == "UNKNOWN":
                if title_in_artist.group(1):
                    artist = artist.replace(title_in_artist.group(1), "").strip()
                    title = title_in_artist.group(1)
                else:
                    artist = artist.replace(title_in_artist.group(2), "").strip()
                    title = title_in_artist.group(2)
                title = title.strip("\":\uFF02'")
                title = title.strip()

            # create formatted file name
            return f"[{artist}][{title}][{features}][{misc}].{filetype}"
