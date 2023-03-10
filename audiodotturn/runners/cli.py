import os
from rich.pretty import pprint
from rich.text import Text
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.console import Console
from audiodotturn import VERSION
from audiodotturn.config import Config, ConfigPath
from audiodotturn.parser import Parser
from audiodotturn.create_tools import Database
from audiodotturn.view_tools import Song, Artist
from audiodotturn.runners.cli_helpers import Creator, Setter, Options
from audiodotturn.errors import AudiodotturnError

class CLI(Setter, Creator, Options):
    """
    A command-line interface runner for audiodotturn

    ...

    Attributes
    ----------
    parsers : Parser
        An instance of the Parser class that is used to parse user passed arguments
    args : Namespace
        A Namespace instance containing the user passed arguments
    config_path : str
        A string containing the path to the configuration file
    config : Config
        An instance of the Config class representing the program configuration
    database : Database
        An instance of the Database class that provides functionality for interacting with the program database

    Methods
    -------
    run()
        Executes the functionality for the user passed command
    """
    def __init__(self):
        # initialize the parser and parse the user passed args
        self.parsers = Parser()
        self.args = self.parsers.parse_args()

        # show version to user
        if self.args.version:
            pprint('audiodotturn version: ' + VERSION)
            exit(1)

        # set the config path
        if self.args.config:
            self.config_path = ConfigPath(self.args.config).get_config_path()
        else:
            self.config_path = ConfigPath().get_config_path()

        # initialize the program configuration
        self.config = Config(self.config_path)

        if self.args.database:
            self.config.program_defaults.database = os.path.join(self.config.program_defaults.directory, self.args.database)

        self.run()
    
    def run(self):
        # show default config settings based on args passed in
        if self.args.defaults:
            self.config.console.print(self.show_defaults(self.config, self.args))

        # show default config options based on args passed in
        elif self.args.options:
            self.config.console.print(self.show_options(self.config, self.args))

        # set command functionality, user can change config settings from cli
        elif self.args.command == 'set':
            if self.args.dry:
                self.config.defaults.program.dry = "true"
                
            self.set_defaults(self.config, self.config_path, self.args)

        # run create commands
        elif self.args.command == 'create':
            # set any parameters passed in by user
            if self.args.extractor:
                self.config.defaults.program.extractor = self.args.extractor

            if self.args.constructor:
                self.config.defaults.program.constructor = self.args.constructor

            if self.args.directory:
                self.config.defaults.program.directory = self.args.directory

            if self.args.dry:
                self.config.defaults.program.dry = "true"

            if self.args.format:
                self.database = Database(self.config)

                result, status = self.format_file(self.database, self.config, file=self.args.format)
                if not self.config.defaults.program.dry:
                    try:
                        self.rename_file(self.config, old=self.args.format, new=result)
                        self.config.console.print(Markdown('# FILE RENAMED SUCCESSFULLY'), markup=True, highlight=True)
                    except IOError as error:
                        AudiodotturnError(error, tuple(self.config.program_defaults.error_msg), self.config.console)
                if status:
                    self.config.console.print(Markdown('# RESULT STATUS: SUCCESS'), markup=True, highlight=True)
                    self.config.console.print(Markdown(f'## DRY_RUN\n### OLD: {self.args.format}\n### NEW: {result}'), markup=True, highlight=True)

                elif status is None:
                    self.config.console.print(Markdown('# RESULT STATUS: NO CHANGE'), markup=True, highlight=True)
                    self.config.console.print(Markdown(f'## DRY_RUN\n### FILE: {self.args.format}\n'), markup=True, highlight=True)

                elif not status:
                    self.config.console.print(Markdown('# RESULT STATUS: ERROR FORMATTING'), markup=True, highlight=True)
                    self.config.console.print(Markdown(f'## DRY_RUN\n### FILE: {self.args.format}\n'), markup=True, highlight=True)

            elif self.args.formatdir:
                self.database = Database(self.config)

                _directory = self.config.program_defaults.directory
                self.format_dir(self.database, self.config)
                changed_md = "## Changed:\n- " + "\n- ".join(self.config.changed)
                unchanged_md = "## No change:\n" + "- " + "\n- ".join(self.config.unchanged)
                error_fmt_md = "## Errors:\n" + "- " + "\n- ".join(self.config.error_fmt)

                changes = None
                prompt = Text(f'\n\nCreate a file listing the changes in {_directory} or view them in the console, or neither? (Short summary of change stats will be shown upon completion regardless)\n', justify="center", style="cyan")
                try:
                    changes = Prompt.ask(prompt, console=self.config.console, choices=["file", "console", "none"])
                except (EOFError, KeyboardInterrupt) as error:
                    AudiodotturnError(error, ("[bold red]Exiting.\n",), self.config.console, if_exit=True)

                if changes.lower() == "console":
                    if len(self.config.changed) > 0:
                        self.config.console.print(Markdown(changed_md + "\n"), markup=True, highlight=True)
                        self.config.console.rule()
                    if len(self.config.unchanged) > 0:
                        self.config.console.print(Markdown(unchanged_md + "\n"), markup=True, highlight=True)
                        self.config.console.rule()
                    if len(self.config.error_fmt) > 0:
                        self.config.console.print(Markdown(error_fmt_md + "\n"), markup=True, highlight=True)
                        self.config.console.rule()

                if changes.lower() == "file":
                    with open(os.path.join(_directory, "format_report.md"), "w") as report_file:
                        console = Console(file=report_file)
                        console.print("# Format Report\n")
                        if len(self.config.changed) >= 1:
                            console.print(changed_md + "\n\n", markup=False)
                        if len(self.config.unchanged) >= 1:
                            console.print(unchanged_md + "\n\n", markup=False)
                        if len(self.config.error_fmt) >= 1:
                            console.print(error_fmt_md + "\n\n", markup=False)
                        console.print("# Short Summary\n")
                        console.print(f"DRY RUN: {self.config.defaults.program.dry.capitalize()}\n")
                        console.print(f"- Changed: {len(self.config.changed)}")
                        console.print(f"- Unchanged: {len(self.config.unchanged)}")
                        console.print(f"- Error Formatting: {len(self.config.error_fmt)}")

                self.config.console.log(f"[white]DRY RUN: {self.config.defaults.program.dry}")
                self.config.console.log(f"[green]Changed: {len(self.config.changed)}")
                self.config.console.log(f"[yellow]Unchanged: {len(self.config.unchanged)}")
                self.config.console.log(f"[red]Error Formatting: {len(self.config.error_fmt)}")
            
            elif self.args.organize:
                self.database = Database(self.config)
                self.organize_by_artist(self.config, self.database, self.config.program_defaults.directory, )

            else:
                self.parsers.create_parser.print_help()
       
        elif self.args.command == "view":
            self.database = Database(self.config)

            if self.args.view_command == "artists":
                artist_viewer = Artist(self.database.c)

                if self.args.tracks:
                    tracks = artist_viewer.get_tracks()
                    if tracks:
                        self.config.console.print(tracks)
                    else:
                        self.config.console.print("[red]No matches found.")

                elif self.args.names:
                    names = artist_viewer.get_artists()
                    if names:
                        self.config.console.print(names)
                    else:
                        self.config.console.print("[red]No matches found.")
                else:
                    self.parsers.view_parser.print_help()

            elif self.args.view_command == "songs":
                song_viewer = Song(self.database.c)

                if self.args.id:
                    _id = song_viewer.search_by_youtube_id(self.args.id)
                    if _id:
                        self.config.console.print(_id)
                    else:
                        self.config.console.print("[red]No matches found.")

                elif self.args.name:
                    name = song_viewer.search_by_title(self.args.name)
                    if name:
                        self.config.console.print(name)
                    else:
                        self.config.console.print("[red]No matches found.")

                elif self.args.artist:
                    artist = song_viewer.search_by_artist(self.args.artist)
                    if artist:
                        self.config.console.print(artist)
                    else:
                        self.config.console.print("[red]No matches found.")

                elif self.args.filetype:
                    filetype = song_viewer.search_by_filetype(self.args.filetype)
                    if filetype:
                        self.config.console.print(filetype)
                    else:
                        self.config.console.print("[red]No matches found.")

                elif self.args.features:
                    features = song_viewer.search_by_features(self.args.features)
                    if features:
                        self.config.console.print(features)
                    else:
                        self.config.console.print("[red]No matches found.")

                elif self.args.misc:
                    misc = song_viewer.search_by_misc(self.args.misc)
                    if misc:
                        self.config.console.print(misc)
                    else:
                        self.config.console.print("[red]No matches found.")

                else:
                    self.parsers.view_parser.print_help()

            else:
                self.parsers.view_parser.print_help()
        
        else:
            self.parsers.parser.print_help()

def main() -> None:
    """
    Get args from main parser    
    Initialize and start the CLI runner

    Returns:
        None
    """
    # Run cli
    CLI()

if __name__ == "__main__":
    main()
