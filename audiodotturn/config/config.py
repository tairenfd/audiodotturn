"""
config.py
---------

The `Config` module contains classes for managing configuration data for AudioDotTurn.

Classes
-------
- `ConfigPath`
- `FormattingDefaults`
- `ProgramDefaults`
- `FormatOptions`
- `ProgramOptions`
- `Options`
- `Defaults`
- `Config`

Notes
-----
None.
"""
import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import rich.progress
import rich.repr
import pkg_resources
from rich.console import Console
from audiodotturn.errors import AudiodotturnError


class ConfigPath:
    """
    Class used to initialize CONFIG_PATH for audiodotturn config.

    Attributes:
        ADT_CONFIG_PATH (list): List of default paths to audiodotturn config file.

    Methods:
        __init__(self, path=None): Constructor for ConfigPath class.
        _set_config_path(self): Set config path based on ADT_CONFIG_PATH or provided path.
        get_config_path(self): Get the path to the audiodotturn config file.
        set_config_path(self, path): Set the path to the audiodotturn config file.
    """
    ADT_CONFIG_PATH = [
        os.path.expanduser("~/.config/audiodotturn/adt_config.json"),
        os.path.expanduser("~/config/audiodotturn/adt_config.json"),
        os.path.expanduser("~/audiodotturn/adt_config.json"),
        os.path.expanduser("~/adt_config.json"),
        "/usr/local/etc/audiodotturn/adt_config.json",
        "/etc/audiodotturn/adt_config.json",
    ]

    def __init__(self, path: Optional[str] = None):
        """
        Constructor for ConfigPath class.

        Args:
            path (Optional[str]): Optional path to audiodotturn config file.
                Defaults to None.

        Returns:
            None
        """
        self.console = Console()
        if path and (not os.path.exists(path) or not path.endswith('.json')):
            try:
                raise FileNotFoundError
            except FileNotFoundError as error:
                AudiodotturnError(error, ('[bold red]Error loading supplied config.',), self.console, if_exit=True)


        self.path = path
        self._set_config_path()

    def _set_config_path(self):
        """
        Set config path based on ADT_CONFIG_PATH or provided path.

        Returns:
            None
        """
        if self.path and os.path.exists(self.path):
            self.console.log(f"[bold green]Using provided config path:[/bold green] {self.path}")
            return

        for path in self.ADT_CONFIG_PATH:
            if os.path.exists(path):
                self.path = path
                self.console.log(f"[bold green]Using default user config path:[/bold green] {self.path}")
                return

        if not self.path or not os.path.exists(self.path):
            self.console.log("[bold yellow]No user config found. Falling back to default package config.")

        self.path = pkg_resources.resource_filename(__name__, "config.json")

    def get_config_path(self) -> str:
        """
        Get the path to the audiodotturn config file.

        Returns:
            str: Path to the audiodotturn config file.
        """
        return self.path

    def set_config_path(self, path: str):
        """
        Set the path to the audiodotturn config file.

        Args:
            path (str): New path to audiodotturn config file.

        Returns:
            None
        """
        self.path = path
        self._set_config_path()

@rich.repr.auto
@dataclass
class FormattingDefaults:
    """
    Class for managing formatting defaults.

    Attributes:
        artist (str): Default value for artist.
        title (str): Default value for title.
        features (str): Default value for features.
        misc (str): Default value for misc.
        youtube_id (str): Default value for YouTube ID.
        filetype (str): Default value for filetype.
    """
    artist: str
    title: str
    features: str
    misc: str
    youtube_id: str
    filetype: str

    def __init__(self, data: Dict[str, str]):
        self.artist = data["artist"]
        self.title = data["title"]
        self.features = data["features"]
        self.misc = data["misc"]
        self.youtube_id = data["youtube_id"]
        self.filetype = data["filetype"]

@rich.repr.auto
@dataclass
class ProgramDefaults:
    """
    Class for managing program defaults.

    Attributes:
        dry (bool): Default value for dry run mode.
        database (str): Default value for database path.
        directory (str): Default value for directory path.
        extractor (str): Default value for extractor.
        constructor (str): Default value for constructor.
        error_msg (list): Default value for error messages.
        exts (list): Default value for file extensions.
    """
    dry: bool
    database: str
    directory: str
    extractor: str
    constructor: str
    error_msg: List[str]
    exts: List[str]

    def __init__(self, data: Dict[str, str]):
        self.dry = data["dry"] == ("true" or True)
        self.database= data["database"]
        self.directory = data["directory"]
        self.extractor = data["extractor"]
        self.constructor = data["constructor"]
        self.error_msg = data["error_msg"]
        self.exts = data["exts"]

@rich.repr.auto
@dataclass
class FormatOptions:
    """
    Class for managing formatting options.

    Attributes:
        description (str): Description of format options.
        all (str): Option for formatting all files.
    """
    description: str
    all: str

    def __init__(self, data: Dict[str, str]):
        self.description = data["description"]
        self.all = data["all"]

@rich.repr.auto
@dataclass
class ProgramOptions:
    """
    Class for managing program options.

    Attributes:
        dry (dict): Dictionary for dry run mode option.
        error_msg (dict): Dictionary for error messages option.
        database (dict): Dictionary for database path option.
        extractor (dict): Dictionary for extractor option.
        constructor (dict): Dictionary for constructor option.
        directory (dict): Dictionary for directory path option.
        exts (dict): Dictionary for file extensions option.
    """
    dry: Dict[str, str]
    error_msg: Dict[str, str]
    database: Dict[str, str]
    extractor: Dict[str, str]
    constructor: Dict[str, str]
    directory: Dict[str, str]
    exts: Dict[str, str]

    def __init__(self, data: Dict[str, Any]):
        self.dry = data["dry"]
        self.error_msg = data["error_msg"]
        self.filename = data["database"]
        self.extractor = data["extractor"]
        self.constructor = data["constructor"]
        self.directory = data["directory"]
        self.exts = data["exts"]

@rich.repr.auto
@dataclass
class Options:
    """
    Class for config options.

    Attributes:
        formatting (FormatOptions): Formatting options.
        program (ProgramOptions): Program options.
    """
    formatting: FormatOptions = field(default_factory=dict)
    program: ProgramOptions = field(default_factory=dict)

@rich.repr.auto
@dataclass
class Defaults:
    """
    Class for config defaults.

    Attributes:
        formatting (FormattingDefaults): Formatting defaults.
        program (ProgramDefaults): Program defaults.
    """
    formatting: FormattingDefaults = field(default_factory=FormattingDefaults)
    program: ProgramDefaults = field(default_factory=ProgramDefaults)

@rich.repr.auto
@dataclass
class Config:
    """
    Class for managing configuration data for AudioDotTurn.

    Attributes:
        console (Console): Console object.
        config (Dict[str, Dict[str, str]]): Configuration data.
        defaults (Defaults): Default values.
        format_defaults (FormattingDefaults): Formatting defaults.
        program_defaults (ProgramDefaults): Program defaults.
        options (Options): Configuration options.
        format_options (FormatOptions): Formatting options.
        program_options (ProgramOptions): Program options.
        changed (List): List of changed configuration values.
        unchanged (List): List of unchanged configuration values.
        error_fmt (List): List of configuration errors.

    Methods:
        __init__(self, config_path): Constructor for Config class.
    """
    console: Console = Console()
    config: Dict[str, Dict[str, str]] = field(default_factory=dict)

    defaults: Defaults = field(default_factory=Defaults)
    format_defaults: FormattingDefaults = field(default_factory=FormattingDefaults)
    program_defaults: ProgramDefaults = field(default_factory=ProgramDefaults)

    options: Options = field(default_factory=Options)
    format_options: FormatOptions = field(default_factory=FormatOptions)
    program_options: ProgramOptions = field(default_factory=ProgramOptions)

    changed: List = field(default_factory=list)
    unchanged: List = field(default_factory=list)
    error_fmt: List = field(default_factory=list)

    def __init__(self, config_path: str):
        """
        Constructor for Config class.

        Returns:
            None
        """
        self.config_path = config_path

        try:
            with rich.progress.open(self.config_path, "r", encoding='utf-8') as conf:
                self.config = json.load(conf)

            self.format_defaults = FormattingDefaults(self.config["settings"]["formatting"])
            self.program_defaults = ProgramDefaults(self.config["settings"]["program"])
            self.defaults = Defaults(
                self.format_defaults,
                self.program_defaults
            )

            for id, ext in enumerate(self.program_defaults.exts):
                self.program_defaults.exts[id] = ext.strip()

            for id, error_type in enumerate(self.program_defaults.error_msg):
                self.program_defaults.error_msg[id] = error_type.strip()

            self.format_options = FormatOptions(self.config["options"]["formatting"])
            self.program_options = ProgramOptions(self.config["options"]["program"])
            self.options = Options(
                self.format_options,
                self.program_options,
            )

            self.changed = []
            self.unchanged = []
            self.error_fmt = []
    
        except KeyError as error:
            self.console.log(
                '\n[bold red]Config file not configured correctly. Make sure all values are set, refer to the default config or the docs for examples.')
            AudiodotturnError(error, ("error",), self.console, if_exit=True)
