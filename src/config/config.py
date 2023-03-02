import os
import sys
import json
import pkg_resources
from rich.table import Table
from rich.console import Console

# Check common configuration paths
ADT_CONFIG_PATH = [
    "/etc/audiodotturn/config.json",
    "/usr/local/etc/audiodotturn/config.json",
    os.path.expanduser("~/.config/audiodotturn/config.json"),
]

CONFIG_PATH = None

# if json is found in a common path, use it
for path in ADT_CONFIG_PATH:
    if os.path.exists(path):
        CONFIG_PATH = path
        break

# if no json in common path use default
if CONFIG_PATH is None:
    CONFIG_PATH = pkg_resources.resource_filename(__name__, "config.json")

(
    artist,
    title,
    features,
    misc,
    youtube_id,
    filetype,
    dry,
    filename,
    directory,
    formatter,
    error_msg,
    exts,
) = (None, None, None, None, None, None, None, None, None, None, None, None)

# read data from json and set defaults
with open(CONFIG_PATH, "r") as c:
    config = json.load(c)
    options = config["options"]
    settings = config["settings"]

    artist = settings["formatting_defaults"]["artist"]
    title = settings["formatting_defaults"]["title"]
    features = settings["formatting_defaults"]["features"]
    misc = settings["formatting_defaults"]["misc"]
    youtube_id = settings["formatting_defaults"]["youtube_id"]
    filetype = settings["formatting_defaults"]["filetype"]

    dry = settings["program_defaults"]["dry"]
    filename = settings["program_defaults"]["filename"]
    directory = settings["program_defaults"]["directory"]
    formatter = settings["program_defaults"]["formatter"]
    error_msg = settings["program_defaults"]["error_msg"]
    exts = tuple(settings["program_defaults"]["exts"].split(", "))


class Config:
    def __init__(self):
        self.console = Console()
        self.directory = directory
        self.formatter = formatter
        self.dry = dry
        self.filename = filename
        self.msg = ""
        self.error_msg = error_msg
        self.exts = exts

        self.artist = artist
        self.title = title
        self.features = features
        self.misc = misc
        self.youtube_id = youtube_id
        self.filetype = filetype

        self.defaults = config
        self.settings = settings
        self.options = options

    def display_all(self) -> None:
        table = Table(title="Configurations", style="bold magenta")
        table.add_column("Section", justify="center", style="cyan")
        table.add_column("Config", justify="center", style="cyan")
        for key in self.defaults:
            if key == "settings":
                subtable = Table(style="blue")
                subtable.add_column("Setting", justify="center", style="magenta")
                subtable.add_column("Value", justify="center", style="magenta")
                for subkey, subval in self.settings.items():
                    if isinstance(subval, dict):
                        for subsubkey, subsubval in subval.items():
                            subtable.add_row(f"{subkey} - {subsubkey}", str(subsubval))
                    else:
                        subtable.add_row(subkey, str(subval))
                table.add_row("Current Defaults", subtable)
            elif key == "options":
                subtable = Table(style="green")
                subtable.add_column("Option", justify="center", style="yellow")
                subtable.add_column("Value", justify="center", style="yellow")
                for subkey, subval in self.options.items():
                    if isinstance(subval, dict):
                        for subsubkey, subsubval in subval.items():
                            subtable.add_row(f"{subkey} - {subsubkey}", str(subsubval))
                    else:
                        subtable.add_row(subkey, str(subval))
                table.add_row("Options", subtable)
        self.console.log(table)

    # Display formatting defaults in a formatted table
    def display_formatting_defaults(self) -> None:
        table = Table(title="Formatting Defaults", style="bold blue")
        table.add_column("Setting", style="magenta")
        table.add_column("Value", style="magenta")

        for key in self.settings["formatting_defaults"]:
            table.add_row(key, self.settings["formatting_defaults"][key])
        self.console.log(table)

    # Display program defaults in a formatted table
    def display_program_defaults(self) -> None:
        table = Table(title="Program Defaults", style="bold green")
        table.add_column("Setting", style="yellow")
        table.add_column("Value", style="yellow")

        for key in self.settings["program_defaults"]:
            table.add_row(key, self.settings["program_defaults"][key])
        self.console.log(table)

    # Display options in a formatted table
    def display_options(self) -> None:
            table = Table(title="Options", show_header=True, header_style="bold magenta")
            table.add_column("Option", style="cyan")
            table.add_column("Value", style="magenta")

            for key in self.options:
                if isinstance(self.options[key], dict):
                    for subkey in self.options[key]:
                        table.add_row(f"{key} - {subkey}", str(self.options[key][subkey]))
                else:
                    table.add_row(key, str(self.options[key]))
            self.console.print(table)

    def write_config(self, dry: bool = dry) -> None:
        if dry:
            self.console.log("\n\n[yellow]DRY RUN MODE. NO CHANGES WILL BE WRITTEN TO THE CONFIG FILE.[/yellow]\n\n" + "Hypothetical config created:\n\n" + json.dumps(self.defaults, indent=4))
            return
        
        with open(CONFIG_PATH, "w") as c:
            json.dump(self.defaults, c, indent=4)
        
        self.console.log("\n\n[green]CHANGES SAVED TO THE CONFIG FILE.[/green]")
        sys.exit(1)

    def set_artist(self, artist: str) -> None:
        self.defaults["settings"]["formatting_defaults"]["artist"] = artist

    def set_title(self, title: str) -> None:
        self.defaults["settings"]["formatting_defaults"]["title"] = title

    def set_features(self, features: str) -> None:
        self.defaults["settings"]["formatting_defaults"]["features"] = features

    def set_misc(self, misc: str) -> None:
        self.console.log(self.defaults["settings"]["formatting_defaults"]["misc"], f'trying to make {misc}')
        self.defaults["settings"]["formatting_defaults"]["misc"] = misc

    def set_youtube_id(self, youtube_id: str) -> None:
        self.defaults["settings"]["formatting_defaults"]["youtube_id"] = youtube_id

    def set_filetype(self, filetype: str) -> None:
        self.defaults["settings"]["formatting_defaults"]["filetype"] = filetype

    def set_dry_set(self, dry_set: bool) -> None:
        self.defaults["settings"]["program_defaults"]["dry"] = dry_set

    def set_filename(self, filename: str) -> None:
        self.defaults["settings"]["program_defaults"]["filename"] = filename

    def set_directory(self, directory: str) -> None:
        self.defaults["settings"]["program_defaults"]["directory"] = directory

    def set_formatter(self, formatter: str) -> None:
        self.defaults["settings"]["program_defaults"]["formatter"] = formatter

    def set_error_msg(self, error_msg: str) -> None:
        self.defaults["settings"]["program_defaults"]["error_msg"] = error_msg

    def set_exts(self, exts: str) -> None:
        self.defaults["settings"]["program_defaults"]["exts"] = exts