import json
import os
import pkg_resources
from rich.json import JSON
from rich.console import Console

# Check common configuration paths
ADT_CONFIG_PATH = [
    "/etc/audiodotturn/config.json",
    "/usr/local/etc/audiodotturn/config.json",
    os.path.expanduser("~/.config/audiodotturn/config.json"),
]

config_path = None

# if json is found in a common path, use it
for path in ADT_CONFIG_PATH:
    if os.path.exists(path):
        config_path = path
        break

# if no json in common path use default
if config_path is None:
    config_path = pkg_resources.resource_filename(__name__, 'config.json')

artist, title, features, misc, youtube_id, filetype, dry, filename, directory, formatter, error_msg, exts = None, None, None, None, None, None, None, None, None, None, None, None

# read data from json and set defaults
with open(config_path, 'r') as c:
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
    exts = tuple(settings["program_defaults"]["exts"].split(', '))




class Config:
    def __init__(cls):
        cls.console = Console()
        cls.directory = directory
        cls.formatter = formatter
        cls.dry = dry
        cls.filename = filename
        cls.msg = ''
        cls.error_msg = error_msg
        cls.exts = exts

        cls.artist = artist
        cls.title = title
        cls.features = features
        cls.misc = misc
        cls.youtube_id = youtube_id
        cls.filetype = filetype

        cls.defaults = config
        cls.settings = settings
        cls.options = options

    # display defaults to user
    def display_all(cls):
        return cls.console.print_json(data=cls.defaults)

    def display_settings(cls):
        return cls.console.print_json(data=cls.settings)

    def display_options(cls):
        return cls.console.print_json(data=cls.options)
