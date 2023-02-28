import json
from rich.markdown import Markdown
from rich.console import Console

ADT_CONFIG_PATH = 'config.json'

class Config:
    def __init__(cls, config: str = ADT_CONFIG_PATH):
        with open(config, 'r') as c:
            config = json.load(c)
            cls.artist = config["formatting_defaults"]["artist"]
            cls.title = config["formatting_defaults"]["title"]
            cls.features = config["formatting_defaults"]["features"]
            cls.misc = config["formatting_defaults"]["misc"]
            cls.youtube_id = config["formatting_defaults"]["youtube_id"]
            cls.filetype = config["formatting_defaults"]["filetype"]
            cls.dry = config["program_defaults"]["dry"]
            cls.filename = config["program_defaults"]["filename"]
            cls.directory = config["program_defaults"]["directory"]
            cls.error_msg = config["program_defaults"]["error_msg"]
        cls.msg = ''
        cls.console = Console()

        cls.defaults = f'''

##### Formatting defaults

    - artist = {cls.artist}
    - title = {cls.title}
    - features = {cls.features}
    - misc = {cls.misc}
    - youtube_id = {cls.youtube_id}
    - filetype = {cls.filetype}
            
##### Program defaults
        
    - directory = {cls.directory}
    - dry = {cls.dry}
    - filename = {cls.filename}
    - error_msg = {cls.error_msg}

        '''

    def display(cls):
        return cls.console.print(Markdown(cls.defaults))
