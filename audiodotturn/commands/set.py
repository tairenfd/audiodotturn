import argparse
import json
from rich.json import JSON
from rich.prompt import Confirm
from audiodotturn.config import Config
from audiodotturn.errors import error_handler


class Set(Config):
    """
    A class that provides functionality for setting the default config values.
    """
    def __init__(self, args: argparse.Namespace):
        """
        Initialize the Set class object.

        Args:
            args: An argparse.Namespace object containing the command line arguments passed to the Create class object.

        Returns:
            None
        """
        self.args = args
        super().__init__()

    def run(self):
        """
        Sets the default values for the program options using the other Set methods.
        """
        updated = False
        changes = {
            "changed": [],
            "unchanged": []
        }
        self.console.log(f'\nMaking changes in `{self.config_path}`\n')
        for arg_name, arg_value in vars(self.args).items():
            if arg_name not in ['dry', 'command', 'version', 'default'] and arg_value is not None:
                _store_set = None
                if arg_name == "dry_set":
                    _store_set = arg_name
                    arg_name = "dry"
                self.console.log(f"\n[bold magenta]Changes being made to: [bold cyan]{arg_name} -> [bold green]{str(arg_value)} [bold magenta]from [bold blue]{getattr(self, arg_name)}\n")
                try:
                    confirmed = Confirm.ask(prompt="\n        [bold white]Are you sure you want to make these changes?\n", console=self.console)
                except (EOFError, KeyboardInterrupt):
                    self.console.log("\n[bold red]Changes cancelled.\n")
                    self.console.log("[bold red]Exiting.\n")
                    return
                if not confirmed:
                    changes["unchanged"].append(arg_name)
                    self.console.log(f"\n        [yellow]Setting '{arg_name}' will not be changed.\n")
                updated = bool(confirmed)
                if updated:
                    self.console.log(f"\n[bold green] Okay!\n\n        Setting [bold cyan]{arg_name} -> [bold green]{str(arg_value)}\n")
                    if _store_set:
                        arg_name = _store_set
                    changes["changed"].append(arg_name)
                    run = getattr(self, f'set_{arg_name}')
                    run(arg_value)

        self.console.log("[bold green]Short summary of changes: \n", JSON(json.dumps(changes)))
        if changes["changed"]:
            updated = True

        with self.console.status(f"[bold green]Attempting to write to {self.config_path}..."):
            try:
                if updated:
                    self.write_config(dry=self.args.dry)
                    if self.args.dry:
                        self.console.log("\n[green]Defaults would have been updated successfully!")
                    else:
                        self.console.log(f"\n[green]Success! Defaults saved in {self.config_path}!")
                else:
                    self.console.log('\n[green]No changes made!\n')
            except IOError as error:
                self.console.log("\n[red]No settings were updated.\n")
                error_handler(self.error_msg, self.console, error)



    def write_config(self, dry: bool = False) -> None:
        """
        Writes the current configuration data to the JSON file. If dry is True, prints the hypothetical
        changes without actually writing them to the file.

        Args:
            dry: bool flag for dry run
        """
        if dry:
            self.console.log("\n\n[yellow]DRY RUN MODE. NO CHANGES WILL BE WRITTEN TO THE CONFIG FILE.[/yellow]\n\n" + "Hypothetical config created:\n\n" + json.dumps(self.defaults, indent=4))
            return
        try:
            with open(self.config_path, "w", encoding='utf-8') as conf:
                json.dump(self.defaults, conf, indent=4)
        except IOError as error:
            error_handler(self.error_msg, self.console, error)
        
        self.console.log("\n\n[green]CHANGES SAVED TO THE CONFIG FILE.[/green]")

    def set_artist(self, new_artist: str) -> None:
        """
        Sets the default value for artist.

        Args:
            new_artist: string to use as default unknown artist format
        """
        self.defaults["settings"]["formatting_defaults"]["artist"] = new_artist

    def set_title(self, new_title: str) -> None:
        """
        Sets the default value for title.
    
        Args:
            new_title: string to use as default unknown title format
        """
        self.defaults["settings"]["formatting_defaults"]["title"] = new_title

    def set_features(self, new_features: str) -> None:
        """
        Sets the default value for features.

        Args:
            new_features: string to use as default unknown features format
        """
        self.defaults["settings"]["formatting_defaults"]["features"] = new_features

    def set_misc(self, new_misc: str) -> None:
        """
        Sets the default value for misc.

        Args:
            new_misc: string to use as default unknown misc format
        """
        self.defaults["settings"]["formatting_defaults"]["misc"] = new_misc

    def set_youtube_id(self, new_youtube_id: str) -> None:
        """
        Sets the default value for YouTube ID.

        Args:
            new_youtube_id: string to use as default unknown youtube_id format
        """
        self.defaults["settings"]["formatting_defaults"]["youtube_id"] = new_youtube_id

    def set_filetype(self, new_filetype: str) -> None:
        """
        Sets the filetype in the configuration data.

        Args:
            new_filetype: string to use as default unknown filetype format
        """
        self.defaults["settings"]["formatting_defaults"]["filetype"] = new_filetype

    def set_dry_set(self, new_dry_set: bool) -> None:
        """
        Sets the dry flag in the program defaults in the configuration data.

        Args:
            new_dry_set: string with value corresponding to the default dry run status
        """
        self.defaults["settings"]["program_defaults"]["dry"] = new_dry_set

    def set_filename(self, new_filename: str) -> None:
        """
        Sets the filename in the program defaults in the configuration data.

        Args:
            new_filename: string with value corresponding to the default json filename
        """
        self.defaults["settings"]["program_defaults"]["filename"] = new_filename

    def set_directory(self, new_directory: str) -> None:
        """
        Sets the directory in the program defaults in the configuration data.

        Args:
            new_directory: string with value corresponding to the default working directory
        """
        self.defaults["settings"]["program_defaults"]["directory"] = new_directory

    def set_formatter(self, new_formatter: str) -> None:
        """
        Sets the formatter in the program defaults in the configuration data.

        Args:
            new_formatter: string with value corresponding to an avaliable formatter
        """
        self.defaults["settings"]["program_defaults"]["formatter"] = new_formatter

    def set_error_msg(self, new_error_msg: str) -> None:
        """
        Sets the error message in the program defaults in the configuration data.
        
        Args:
            new_error_msg: string formatted as 'option | option | option' with error message formats you'd like audiodotturn to display
        """
        self.defaults["settings"]["program_defaults"]["error_msg"] = new_error_msg

    def set_exts(self, new_exts: str) -> None:
        """
        Sets the extensions in the program defaults in the configuration data.
        
        Args:
            new_exts: string formatted as '.ext1, .ext2, .ext3' with extensions you'd like audiodotturn to format
        """
        self.defaults["settings"]["program_defaults"]["exts"] = new_exts
