import json
from rich.console import Console
from rich.table import Table
from audiodotturn.config.config_path import CONFIG_PATH
from audiodotturn.errors import error_handler

class Config:
    """
    Class for managing configuration data.
    """
    def __init__(self):
        """
        Constructor for Config class. 
        Loads configuration data from JSON file and sets default values.
        """
        self.console = Console()

        # read data from json and set defaults
        try:
            with open(CONFIG_PATH, "r", encoding='utf-8') as c:
                self.defaults = json.load(c)
                self.options = self.defaults["options"]
                self.settings = self.defaults["settings"]

                self.artist = self.settings["formatting_defaults"]["artist"]
                self.title = self.settings["formatting_defaults"]["title"]
                self.features = self.settings["formatting_defaults"]["features"]
                self.misc = self.settings["formatting_defaults"]["misc"]
                self.youtube_id = self.settings["formatting_defaults"]["youtube_id"]
                self.filetype = self.settings["formatting_defaults"]["filetype"]

                self.dry = self.settings["program_defaults"]["dry"]
                self.filename = self.settings["program_defaults"]["filename"]
                self.directory = self.settings["program_defaults"]["directory"]
                self.formatter = self.settings["program_defaults"]["formatter"]
                self.error_msg = self.settings["program_defaults"]["error_msg"].replace(' ', '').split('|')
                self.exts = tuple(self.settings["program_defaults"]["exts"].replace(' ', '').split(","))
                self.config_path = CONFIG_PATH
        except KeyError as error:
            self.console.log('\n[bold red]Config file not configured correctly. Make sure all values are set, refer to the default config or the docs for examples.')
            error_handler(self.error_msg, self.console, error)

    def display_all(self) -> None:
        """
        Displays all configuration data in a formatted table.
        """
        table = Table(title="Configurations", style="bold magenta")
        table.add_column("Section", justify="center", style="cyan", min_width=30)
        table.add_column("Config", justify="center", style="cyan", min_width=20)
        for key in self.defaults:
            if key == "settings":
                subtable = Table(style="blue")
                subtable.add_column("Setting", justify="center", style="magenta", min_width=30)
                subtable.add_column("Value", justify="center", style="magenta", min_width=20)
                for subkey, subval in self.settings.items():
                    if isinstance(subval, dict):
                        for subsubkey, subsubval in subval.items():
                            subtable.add_row(f"{subkey} - {subsubkey}", str(subsubval))
                    else:
                        subtable.add_row(subkey, str(subval))
                table.add_row("Current Defaults", subtable)
            elif key == "options":
                subtable = Table(style="green")
                subtable.add_column("Option", justify="center", style="yellow", min_width=30)
                subtable.add_column("Value", justify="center", style="yellow", min_width=20)
                for subkey, subval in self.options.items():
                    if isinstance(subval, dict):
                        subsubtable = Table(style="blue")
                        subsubtable.add_column('Description', justify="center", style="yellow", min_width=40)
                        subsubtable.add_column('Options', justify="center", style="yellow", min_width=60)
                        for subsubkey, subsubval in subval.items():
                            if isinstance(subsubval, dict):
                                for sub3key, sub3val in subsubval.items():
                                    if isinstance(sub3val, dict):
                                        opts = ''
                                        for key in sub3val:
                                            opts += f'{key} - {sub3val[key]}\n'
                                        sub3val = opts
                                    subsubtable.add_row(f"{subsubkey} - {sub3key}", str(sub3val) + '\n')
                            else:    
                                subsubtable.add_row(f"{str(subkey).title().replace('_', ' ')} - {subsubkey}", str(subsubval) + '\n')

                        table.add_row(f"{str(subkey).title().replace('_', ' ')} Options", subsubtable)

                    else:
                        subtable.add_row(str(subkey).title().replace('_', ' '), str(subval) + '\n')
        self.console.log(table)

    # Display formatting defaults in a formatted table
    def display_formatting_defaults(self) -> None:
        """
        Displays the formatting defaults in a formatted table.
        """
        table = Table(title="Formatting Defaults", style="bold blue")
        table.add_column("Setting", style="magenta", min_width=10)
        table.add_column("Value", style="magenta", min_width=10)

        for key in self.settings["formatting_defaults"]:
            table.add_row(key, self.settings["formatting_defaults"][key])
        self.console.log(table)

    # Display program defaults in a formatted table
    def display_program_defaults(self) -> None:
        """
        Displays the current defaults in a formatted table.
        """
        table = Table(title="Program Defaults", style="bold green")
        table.add_column("Setting", style="yellow", min_width=10)
        table.add_column("Value", style="yellow", min_width=10)

        for key in self.settings["program_defaults"]:
            table.add_row(key, self.settings["program_defaults"][key])
        self.console.log(table)

    # Display options in a formatted table
    def display_options(self) -> None:
        """
        Displays the config options in a formatted table.
        """
        table = Table(title="Options", show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan", justify="center", min_width=30)
        table.add_column("Info", style="magenta", justify="center", min_width=35)
        for subkey, subval in self.options.items():
            if isinstance(subval, dict):
                subsubtable = Table(style="blue")
                subsubtable.add_column('Description', justify="center", style="yellow", min_width=40)
                subsubtable.add_column('Options', justify="center", style="yellow", min_width=60)
                for subsubkey, subsubval in subval.items():
                    if isinstance(subsubval, dict):
                        for sub3key, sub3val in subsubval.items():
                            if isinstance(sub3val, dict):
                                opts = ''
                                for key in sub3val:
                                    opts += f'{key} - {sub3val[key]}\n'
                                sub3val = opts
                            subsubtable.add_row(f"{subsubkey} - {sub3key}", str(sub3val) + '\n')
                    else:    
                        subsubtable.add_row(f"{str(subkey).title().replace('_', ' ')} - {subsubkey}", str(subsubval) + '\n')

                table.add_row(f"{str(subkey).title().replace('_', ' ')} Options", subsubtable)

        self.console.print(table)

#init config
defaults = Config()
