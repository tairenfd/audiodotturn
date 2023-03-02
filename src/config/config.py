import json
import os
import pkg_resources
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

    # display defaults to user
    def display_all(self) -> None:
        return self.console.print_json(data=self.defaults)

    def display_settings(self) -> None:
        return self.console.print_json(data=self.settings)

    def display_options(self) -> None:
        return self.console.print_json(data=self.options)
