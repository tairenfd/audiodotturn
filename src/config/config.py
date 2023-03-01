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

artist, title, features, misc, youtube_id, filetype, dry, filename, directory, error_msg = None, None, None, None, None, None, None, None, None, None

# read data from json and set defaults
with open(config_path, 'r') as c:
    config = json.load(c)

    artist = config["formatting_defaults"]["artist"]
    title = config["formatting_defaults"]["title"]
    features = config["formatting_defaults"]["features"]
    misc = config["formatting_defaults"]["misc"]
    youtube_id = config["formatting_defaults"]["youtube_id"]
    filetype = config["formatting_defaults"]["filetype"]

    dry = config["program_defaults"]["dry"]
    filename = config["program_defaults"]["filename"]
    directory = config["program_defaults"]["directory"]
    error_msg = config["program_defaults"]["error_msg"]




class Config:
    def __init__(cls):
        cls.console = Console()
        cls.directory = directory
        cls.dry = dry
        cls.filename = filename
        cls.msg = ''
        cls.error_msg = error_msg

        cls.artist = artist
        cls.title = title
        cls.features = features
        cls.misc = misc
        cls.youtube_id = youtube_id
        cls.filetype = filetype

        cls.defaults = config

    # display defaults to user
    def display(cls):
        return cls.console.print_json(data=cls.defaults)
