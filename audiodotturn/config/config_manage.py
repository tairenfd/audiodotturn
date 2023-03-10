"""
config_manage.py
----------------

This module contains the `ConfigManager` class, which is responsible for managing configuration settings and writing them to a config file.

Classes
-------
- `ConfigManager`

Notes
-----
None.
"""
import json
from rich.json import JSON
from rich.panel import Panel
from rich.console import Group
from rich.prompt import Confirm
from audiodotturn.config import Config
from audiodotturn.errors import AudiodotturnError


class ConfigManager:
    """
    Class for managing configuration settings and writing them to a config file.

    Args:
        config (Config): An instance of the Config class containing the configuration settings.
        config_path (Optional[str]): Optional path to the config file. Defaults to None.

    Attributes:
        config (Config): An instance of the Config class containing the configuration settings.
        config_path (str): Path to the config file.
        defaults (Defaults): An instance of the Defaults class containing the default configuration settings.
        format_defaults (dict): A dictionary containing the default formatting configuration settings.
        program_defaults (dict): A dictionary containing the default program configuration settings.
        options (Options): An instance of the Options class containing the current configuration settings.
        format_options (FormattingOptions): An instance of the FormattingOptions class containing the current formatting configuration settings.
        program_options (ProgramOptions): An instance of the ProgramOptions class containing the current program configuration settings.
        dry (bool): Current value of the dry setting in ProgramDefaults.
        _dry (None): Used to store the value of dry setting temporarily.
        changes (dict): A dictionary used to track changes made to the configuration settings.

    Raises:
        TypeError: If config argument is not an instance of the Config class.

    Returns:
        None
    """

    def __init__(self, config: Config, config_path: str = None):
        """
        Constructor for ConfigManager class.

        Args:
            config_path (Optional[str]): Optional path to the config file. Defaults to None.

        Returns:
            None
        """
        self.config = config
        self.config_path = config_path or self.config.config_path
        self.defaults = self.config.defaults
        self.format_defaults = self.defaults.formatting.__dict__
        self.program_defaults = self.defaults.program.__dict__
        self.options = self.config.options
        self.format_options = self.options.formatting
        self.program_options = self.options.program
        self.dry = self.defaults.program.dry
        self._dry = None
        self.changes = {
            "Modified": [],
            "Cancelled": []
        }

    def confirm_changes(self, setting, before, after):
        """
        Confirms changes being made to a configuration setting.

        Args:
            setting (str): The name of the setting being changed.
            before (Any): The original value of the setting being changed.
            after (Any): The new value of the setting being changed.

        Returns:
            bool: True if changes are confirmed, False otherwise.
        """
        self.config.console.log(f"\n[bold magenta]Changes being made to: [bold cyan]{setting} -> [bold green]{before} [bold magenta]to [bold blue]{after}\n")
        try:
            confirmed = Confirm.ask(prompt="\n        [bold white]Are you sure you want to make these changes?", console=self.config.console)
        except (EOFError, KeyboardInterrupt) as error:
            self.config.console.log("\n[bold red]Changes cancelled.\n")
            AudiodotturnError(error, ("[bold red]Exiting.\n",), self.config.console, if_exit=True)
        if confirmed:
            self.config.console.log(f"\n        [bold green]Confirmed change: {setting} = {after}.\n")
            self.changes["Modified"].append(f'{setting} changed to {after}')
            return True
        self.changes["Cancelled"].append(f'{setting} will remain as {before}')
        return False

    def set_format_defaults(self, artist=None, title=None, features=None, misc=None, youtube_id=None, filetype=None):
        """
        Set new values for FormattingDefaults and write them to the config file.

        Args:
            artist (Optional[str]): New value for artist in FormattingDefaults. Defaults to None.
            title (Optional[str]): New value for title in FormattingDefaults. Defaults to None.
            features (Optional[str]): New value for features in FormattingDefaults. Defaults to None.
            misc (Optional[str]): New value for misc in FormattingDefaults. Defaults to None.
            youtube_id (Optional[str]): New value for youtube_id in FormattingDefaults. Defaults to None.
            filetype (Optional[str]): New value for filetype in FormattingDefaults. Defaults to None.

        Returns:
            dict: changes made
        """

        current_dry = self.defaults.program.dry
        print(current_dry)
        if artist is not None and artist != self.defaults.formatting.artist:
            if self.confirm_changes("artist", self.defaults.formatting.artist, artist):
                self.defaults.formatting.artist = artist
        if title is not None and title != self.defaults.formatting.title:
            if self.confirm_changes("title", self.defaults.formatting.title, title):
                self.defaults.formatting.title = title
        if features is not None and features != self.defaults.formatting.features:
            if self.confirm_changes("features", self.defaults.formatting.features, features):
                self.defaults.formatting.features = features
        if misc is not None and misc != self.defaults.formatting.misc:
            if self.confirm_changes("misc", self.defaults.formatting.misc, misc):
                self.defaults.formatting.misc = misc
        if youtube_id is not None and youtube_id != self.defaults.formatting.youtube_id:
            if self.confirm_changes("youtube_id", self.defaults.formatting.youtube_id, youtube_id):
                self.defaults.formatting.youtube_id = youtube_id
        if filetype is not None and filetype != self.defaults.formatting.filetype:
            if self.confirm_changes("filetype", self.defaults.formatting.filetype, filetype):
                self.defaults.formatting.filetype = filetype

        if not current_dry and self.changes["Modified"]:
            try:
                with self.config.console.status("[bold green]Working..."):
                    with open(self.config_path, "r+") as conf:
                        data = json.load(conf)
                        data["settings"]["formatting"] = self.defaults.formatting.__dict__
                        conf.seek(0)
                        json.dump(data, conf, indent=4)
                        conf.truncate()
                        self.config.console.log(f"File updated at {self.config_path}")
            except IOError as error:
                AudiodotturnError(error, tuple(self.defaults.program.error_msg), self.config.console, if_exit=True)

        result = Group(
            Panel('\n'.join(self.changes["Modified"]), title="Modified"),
            Panel('\n'.join(self.changes["Cancelled"]), title="Cancelled"),
        )
        config_new = Panel(JSON.from_data(self.defaults.formatting.__dict__), title="Hypothetical New Formatting Section")
        self.config.console.print(result)
        self.config.console.print(config_new)

    def set_program_defaults(self, dry=None, filename=None, directory=None, extractor=None, constructor=None, error_msg=None, exts=None):
        """
        Set new values for ProgramDefaults and write them to the config file.

        Args:
            dry (Optional[bool]): New value for dry in ProgramDefaults. Defaults to None.
            filename (Optional[str]): New value for filename in ProgramDefaults. Defaults to None.
            directory (Optional[str]): New value for directory in ProgramDefaults. Defaults to None.
            extractor (Optional[str]): New value for extractor in ProgramDefaults. Defaults to None.
            constructor (Optional[str]): New value for constructor in ProgramDefaults. Defaults to None.
            error_msg (Optional[Tuple[str]]): New value for error_msg in ProgramDefaults. Defaults to None.
            exts (Optional[Tuple[str]]): New value for exts in ProgramDefaults. Defaults to None.

        Returns:
            None
        """
        current_dry = self.defaults.program.dry
        if filename is not None:
            if self.confirm_changes("filename", self.defaults.program.filename, filename):
                self.defaults.program.filename = filename
        if dry is not None:
            if self.confirm_changes("dry", self.defaults.program.dry, dry):
                self.defaults.program.dry = dry
        if directory is not None:
            if self.confirm_changes("directory", self.defaults.program.directory, directory):
                self.defaults.program.directory = directory
        if extractor is not None:
            if self.confirm_changes("extractor", self.defaults.program.extractor, extractor):
                self.defaults.program.extractor = extractor
        if constructor is not None:
            if self.confirm_changes("constructor", self.defaults.program.constructor, constructor):
                self.defaults.program.constructor = constructor
        if error_msg is not None:
            if self.confirm_changes("error_msg", self.defaults.program.error_msg, error_msg):
                self.defaults.program.error_msg = error_msg.replace(' ', '').split(',')
        if exts is not None:
            if self.confirm_changes("exts", self.defaults.program.exts, exts):
                self.defaults.program.exts = exts.replace(' ', '').split(',')

        if not current_dry and self.changes["Modified"]:
            try:
                with self.config.console.status("[bold green]Working..."):
                    with open(self.config_path, "r+") as conf:
                        data = json.load(conf)
                        data["settings"]["program"] = self.defaults.program.__dict__
                        conf.seek(0)
                        json.dump(data, conf, indent=4)
                        conf.truncate()
            except IOError as error:
                AudiodotturnError(error, tuple(self.defaults.program.error_msg), self.config.console, if_exit=True)

        result = Group(
            Panel('\n'.join(self.changes["Modified"]), title="Modified"),
            Panel('\n'.join(self.changes["Cancelled"]), title="Cancelled"),
        )
        config_new = Panel(JSON.from_data(self.defaults.program.__dict__), title="Hypothetical New Program Section")
        self.config.console.print(result)
        self.config.console.print(config_new)
