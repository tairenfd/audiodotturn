"""
cli_helpers.py
--------------

This module provides helper classes for the command-line interface of the AudioDotTurn application.

Classes
-------
- `Setter`
- `Creator`
- `Options`

Notes
-----
Note.
"""
import os
import json
import shutil
import re
import sqlite3
from rich import box
from rich.panel import Panel
from rich.console import Group
from rich.prompt import Confirm, IntPrompt
from rich.json import JSON
from audiodotturn.config import Config, ConfigManager
from audiodotturn.errors import AudiodotturnError
from audiodotturn.create_tools import StandardExtractor, Constructors, Database

class Setter:
    """
    The Setter class provides a method for setting the default values for the AudioDotTurn application using the given command-line arguments.

    Methods:
        set_defaults(config: Config, config_path: str, args) -> None:
        Sets the default values for the AudioDotTurn application using the given CLI arguments.

    Args:
        config (Config): The configuration object to update with new default values.
        config_path (str): The path to the configuration file.
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    def set_defaults(self, config: Config, config_path: str, args):
        '''
        Sets the default values for the audio formatting application using the given CLI arguments.
        
        Args:
            config (Config): The configuration object to update with new default values.
            config_path (str): The path to the configuration file.
            args (argparse.Namespace): The parsed command-line arguments.

        Returns:
            None
        '''
        setter = ConfigManager(config, config_path)

        artist = args.artist or None
        title = args.title or None
        features = args.features or None
        misc = args.misc or None
        youtube_id = args.youtube_id or None
        filetype = args.filetype or None

        format_changes = any((artist, title, features, misc, youtube_id, filetype))

        dry = args.dryset or None
        database = args.data or None
        directory = args.directory or None
        extractor = args.extractor or None
        constructor = args.constructor or None
        error_msg = args.errormsg or None
        exts = args.exts or None

        program_changes = any((dry, database, directory, extractor, constructor, error_msg, exts))

        if format_changes:
            try:
                confirmed = Confirm.ask(prompt="\n[bold white]Enter editor for format defaults?\n", console=config.console)
            except (EOFError, KeyboardInterrupt) as error:
                config.console.log("\n[bold red]Formatting changes cancelled.\n")
                if not program_changes:
                    AudiodotturnError(error, ("[bold red]Exiting.\n",), config.console, if_exit=True)
            if confirmed:
                setter.set_format_defaults(artist, title, features, misc, youtube_id, filetype)


        if program_changes:
            try:
                confirmed = Confirm.ask(prompt="\n[bold white]Enter editor for program defaults?\n", console=config.console)
            except (EOFError, KeyboardInterrupt) as error:
                config.console.log("\n[bold red]Program changes cancelled.\n")
                AudiodotturnError(error, ("[bold red]Exiting.\n",), config.console, if_exit=True)
            if confirmed:
                setter.set_program_defaults(dry, database, directory, extractor, constructor, error_msg, exts)

class Creator:
    """
    The Creator class provides methods for formatting audio files in the directory specified in the program's configuration object.

    Methods
    -------
        format_dir(database: Database, config: Config) -> None:
        Formats all audio files in the directory specified in the program's configuration object.

            Args:
                database (Database): The database object for storing audio file information.
                config (Config): The program's configuration object.

            Returns:
                None

        format_file(database: Database, config: Config, file: str, dirs: bool = False) -> tuple:
        Formats an audio file.

            Args:
                database (Database): The database object for storing audio file information.
                config (Config): The program's configuration object.
                file (str): The audio file to format.
                dirs (bool, optional): Whether or not the file is in a directory. Defaults to False.

            Returns:
                Tuple with file name and status of formatting.

        extraction(config: Config, file: str, extractor: str) -> tuple:
        Extracts information from an audio file using the set extractor.

            Args:
                config (Config): The program's configuration object.
                file (str): The audio file to extract information from.
                extractor (str): The audio extractor to use.

            Returns:
                Tuple with extracted information and extraction status.

        rename_file(config: Config, old: str, new: str) -> None:
        Renames an audio file.

            Args:
                config (Config): The program's configuration object.
                old (str): The current file name.
                new (str): The new file name.

            Returns:
                None
    """
    def format_dir(self, database: Database, config: Config):
        '''
        Formats all audio files in the directory specified in the program's configuration object.

        Args:
            database (Database): The database object for storing audio file information.
            config (Config): The program's configuration object.

        Returns:
            None
        '''
        confirmed = Confirm.ask(f"Dry mode is currently: {config.program_defaults.dry}\nWould you like to create database entries? This must be confirmed regardless of dry run status.", console=config.console)
        if confirmed:
            data_dirs = True
        else:
            data_dirs = False

        for root, dirs, files in os.walk(config.defaults.program.directory):
            for filename in files:
                if filename.endswith(tuple(config.defaults.program.exts)):
                    config.defaults.program.directory = root
                    result, status = self.format_file(database=database, config=config, file=filename, dirs=True, dir_data=data_dirs)
                    if status is None:
                        config.unchanged.append(result)
                    elif not status:
                        config.error_fmt.append(result)
                    elif status:
                        if not self.config.defaults.program.dry:
                                rename_status = self.rename_file(self.config, old=filename, new=result)
                        config.changed.append(rename_status)
                else:
                    config.error_fmt.append(filename)
        database.close_db()

    def format_file(self, database: Database, config: Config, file: str, dirs: bool = False, dir_data: bool = False):
        '''
        Format a file
        '''
        extractor = config.defaults.program.extractor
        with config.console.status("[bold green]Extracting data..."):
            extracted_data, status = self.extraction(config=config, file=file, extractor=extractor)

        if status is False:
            return (file, status)

        # all construction happens in Constructors class, it will return a list of formatting options
        constructor = Constructors(extracted_data, config.defaults.program.constructor)
        with config.console.status("[bold green]Constructing..."):
            options = constructor.run()

        if status or status is None and not dirs:
            if config.program_defaults.dry and not dirs:
                confirmed = Confirm.ask(prompt="\n[bold white]Construction successful! You're in dry run mode, would you like to update the database anyways?\n", console=config.console).__bool__()
                if confirmed:
                    database.add_data_to_db(extracted_data)
            elif not config.program_defaults.dry and not dirs:
                confirmed = Confirm.ask(prompt="\n[bold white]Construction successful! Add the track data to the database?\n", console=config.console).__bool__()
                if confirmed:
                    database.add_data_to_db(extracted_data)
    
        if dir_data and dirs and (status or status is None):
            database.add_data_to_db(extracted_data)

        # multifile, autoselects final option in list - contains most info
        if status and dirs:
            return (options[-1], status)
        elif status is None and dirs:
            return (file, status)

        # single file, interactive choice menu
        if status and not dirs or status is None and not dirs:
            config.console.print("[magenta]options = \n")
            for i, option in enumerate(options):
                config.console.print(f" - {i + 1}    {option}\n", markup=False, style="cyan")
            while True:
                try:
                    choice = IntPrompt.ask("Which would you like to use?").real
                    if choice > len(options) or choice < 0:
                        raise TypeError('Invalid choice')
                    choice = choice - 1
                    break
                except (EOFError, KeyboardInterrupt) as error:
                    config.console.log("\n[bold red]Program changes cancelled.\n")
                    AudiodotturnError(error, ("[bold red]Exiting.\n",), config.console, if_exit=True)
                except TypeError as error:
                    config.console.log(f'[red]{error}')

            database.close_db()
            if options[choice] == file:
                return (options[choice], None)
            return (options[choice], True)

    def extraction(self, config: Config, file: str, extractor: str):
        '''
        extract info from file using the set extractor
        '''
        try:
            standard_extract = StandardExtractor(config, extractor)
            file, status = standard_extract.extract(file)
            return (file, status)
        except TypeError as error:
            AudiodotturnError(error, tuple(config.defaults.program.error_msg), config.console, if_exit=True)

    def rename_file(self, config: Config, old: str, new: str) -> None:
        status = f"Unsucessfully renamed {old} to {new}"
        with config.console.status("[bold green]Formatting filename..."):
            try:
                os.rename(
                    config.defaults.program.directory.rstrip('/') + "/" + old, config.defaults.program.directory.rstrip('/') + "/" + new
                )
                status = f'{old} has been formatted to {new} in {config.defaults.program.directory}'
            except (OSError) as error:
                AudiodotturnError(error, tuple(config.defaults.program.error_msg), config.console, if_exit=True)
        return status

    def organize_by_artist(self, config: Config, database: Database, audio_dir: str) -> None:
        """
        Organize audio files by artist in a case-insensitive manner.

        Args:
            config (Config): initialized Config class.
            database (Database): initialized Database class.
            audio_dir (str): The directory containing the audio files.

        Returns:
            None
        """
        # Get a list of all artists
        try:
            database.c.execute("SELECT * FROM artists")
        except sqlite3.OperationalError as error:
            AudiodotturnError(error, tuple(config.program_defaults.error_msg), config.console, if_exit=True)

        try:
            artists = [row[0] for row in database.c.fetchall()]
            if not artists:
                raise TypeError("Seems as though the database is empty, do a dry run of the directory formatter or file formatter to add items to database")
        except TypeError as error:
            AudiodotturnError(error, tuple(config.program_defaults.error_msg), config.console, if_exit=True)

        confirmed = Confirm.ask(prompt=f"\n[bold yellow]THIS WILL CREATE AND MOVE FILES IN YOUR SYSTEM IF YOU ARE NOT IN DRY RUN (currently dry={config.program_defaults.dry}). CONTINUE?\n", console=config.console).__bool__()
        if not confirmed:
            config.program_defaults.dry = True

        files = set()
        created = []
        artist_dir = ""

        for artist in artists:
            artist_dir = os.path.join(audio_dir, artist.replace(' ',''))
                
            for filename in os.listdir(audio_dir):
                if filename.endswith(tuple(config.program_defaults.exts)):
                    match = re.match(
                        r"\[(.+?)\].*$", filename
                    )
                    if not match:
                        match = re.match(
                            r"(.+?) -.*$", filename
                        )
                    if match:
                        artist = match.group(1)
                        files.add((artist, filename))
                        artist_dir = os.path.join(audio_dir, artist.replace(' ','_'))
                        os.mkdir(artist_dir)
                        created.append(artist_dir)
                        print(artist_dir)

                    # if dry run, no files will be moved and no directories created,
                    # the user just get the data of what wouldve been changed if applied
                    if not config.program_defaults.dry:
                        print(f"{audio_dir}{filename}", f"{artist_dir}/")
                        try:
                            shutil.move(
                                f"{audio_dir}{filename}", f"{artist_dir}/"
                            )
                        except FileExistsError:
                            pass

        if config.program_defaults.dry:
            config.console.print(f'Would have moved {len(files)} files\n', f'Directories that would have been created in {audio_dir}:\n- {created}')
        else:
            config.console.print(f'Moved {len(files)} files\n', f'Directories that have been created in {audio_dir}:\n- {created}')




class Options:
    def show_defaults(self, config: Config, args):
        """
        Shows the default values for the program and formatting.
    
        Returns:
            None
        """
        display = args.defaults
        if display == 'program':
            return Panel.fit(JSON(json.dumps(config.program_defaults.__dict__), highlight=True, indent=4, sort_keys=True), box = box.HEAVY_HEAD, title= "Program Defaults", title_align="center")
        elif display == 'format':
            return Panel.fit(JSON(json.dumps(config.format_defaults.__dict__), highlight=True, indent=4, sort_keys=True), box = box.HEAVY_HEAD, title= "Format Defaults", title_align="center")
        else:
            panels = Group(
                Panel.fit(JSON(json.dumps(config.program_defaults.__dict__), highlight=True, indent=4, sort_keys=True), width=30, box = box.HEAVY_HEAD, title= "Program Defaults", title_align="center"),
                Panel.fit(JSON(json.dumps(config.format_defaults.__dict__), highlight=True, indent=4, sort_keys=True), width=30, box = box.HEAVY_HEAD, title= "Format Defaults", title_align="center"),
                fit=True
            )
            return panels

    def show_options(self, config: Config, args):
        """
        Shows the available options and descriptions for the program and formatting values.
    
        Returns:
            None
        """
        display = args.options
        if display == 'program':
            return Panel(JSON(json.dumps(config.program_options.__dict__), highlight=True, indent=4, sort_keys=True), box = box.HEAVY_HEAD, title= "Program Options", title_align="center")
        elif display == 'format':
            return Panel(JSON(json.dumps(config.format_options.__dict__), highlight=True, indent=4, sort_keys=True), box = box.HEAVY_HEAD, title= "Format Options", title_align="center")
        else:
            panels = Group(
                Panel(JSON(json.dumps(config.program_options.__dict__), highlight=True, indent=4, sort_keys=True), box = box.HEAVY_HEAD, title= "Program Options", title_align="center"),
                Panel(JSON(json.dumps(config.format_options.__dict__), highlight=True, indent=4, sort_keys=True), box = box.HEAVY_HEAD, title= "Format Options", title_align="center"),
                fit=True
            )
            return panels
