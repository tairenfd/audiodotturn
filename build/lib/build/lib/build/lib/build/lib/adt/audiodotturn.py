from typing import List, Dict, Any
from io import StringIO
from datetime import datetime
from rich.console import Console
from adt.config import ConfigUser
from adt.construct import Constructor
from adt.extract import Extractor
from adt.database import Database


class AudioDotTurn:
    def __init__(self, config_path: str = None, db_path: str = None):
        self.config = ConfigUser(config_path)
        self.extractor = Extractor(self.config.exts, self.config.output_opts)
        self.database = Database(db_path or self.config.db_path)
        self.current_data = None
        self.constructor = None

    def extract_files(self, files: List[str], output_format: str = "dict") -> List[Any]:
        """
        Extracts metadata from multiple audio files and returns a list of dictionaries which
        contain the data or a list of the data in the chosen format.
        """
        self.current_data = self.extractor.extract_complex_list(files, output_format)
        return self.current_data

    def extract_file(self, file: str, opt: str = "dict") -> List[Any]:
        """
        Extracts metadata from a single audio file and returns a list containing a single
        dictionary containing the data.
        """
        self.extractor.complex_extract(file)
        self.current_data = self.extractor.get_extraction(opt)
        return [self.current_data]

    def update_database(self, data: List[Dict] = None) -> None:
        """
        Updates the database with data extracted from audio files.
        """
        self.database.create_database()
        self.database.create_tables()
        return self.database.update_database(data or self.current_data)
    
    def produce_construct_report(self, results, console, args):
        """
        Produce report of constructions. Options are html, svg, txt, or console.

        ONLY FOR USE WITH CLI CLIENT        
        """
        success = 0
        failure = 0

        report_type = input(
            "\nHow would you like to process the constructions(s)?\nOutput will be sent to working directory named 'construct_report.[ext]' if a file.\nOptions: html, text, svg, console\nFor none press enter. "
        )
        match report_type.lower().strip():
            case "html":
                report_type = "html"
            case "svg":
                report_type = "svg"
            case "text":
                report_type = "text"
            case "console":
                report_type = "console"
            case _:
                report_type = None

        if report_type is not None:
            if report_type == "console":
                if not args.auto:
                    if results["success"]:
                        if args.multi:
                            for result in results["success"]:
                                console.print(f"\n[cyan]Original File: [magenta]{result[0]}\n")
                                console.print("Options created:", style="cyan")
                                for option in result[1]:
                                    console.print(option, style="success")
                                success += 1
                        else:
                            console.print(f"\nOriginal File: {results['success'][0][0]}\n")
                            console.print("Options created:", style="cyan")
                            for option in results["success"][0][1]:
                                console.print(option, style="success")
                            success += 1
                        console.print('\n')
                else:
                    if results["success"]:
                        if args.multi:
                            for result in results["success"]:
                                console.print(f'[magenta]"{result[0]}" => [success]"{result[1]}"\n')
                            success += 1
                        else:
                            console.print(f'[magenta]{results["success"][0][0]} => [success]{results["success"][0][1]}', style="success")
                            success += 1

                        console.print('\n')

                if results["failure"]:
                    for result in results["failure"]:
                        failure += 1
                        console.print(f"\nFailed to construct: {result}\n", style="failure")
            else:
                record_console = Console(record=True, stderr=True, file=StringIO())
                if not args.auto:
                    if results["success"]:
                        if args.multi:
                            for result in results["success"]:
                                record_console.print(f"\n[cyan]Original File: [magenta]{result[0]}\n")
                                record_console.print("Options created:", style="cyan")
                                for option in result[1]:
                                    record_console.print(option, style="green")
                                success += 1
                        else:
                            record_console.print(f"\nOriginal File: {results['success'][0][0]}\n")
                            record_console.print("Options created:", style="cyan")
                            for option in results["success"][0][1]:
                                record_console.print(option, style="green")
                            success += 1
                        record_console.print('\n')
                else:
                    if results["success"]:
                        if args.multi:
                            for result in results["success"]:
                                record_console.print(f'[magenta]"{result[0]}" => [green]"{result[1]}"\n')
                                success += 1
                        else:
                            record_console.print(f'[magenta]{results["success"][0][0]} => [success]{results["success"][0][1]}', style="success")
                            success += 1

                        record_console.print('\n')

                if results["failure"]:
                    for result in results["failure"]:
                        failure += 1
                        record_console.print(f"\nFailed to construct: {result}\n", style="red")

                match report_type:
                    case "html":
                        record = record_console.export_html()
                    case "svg":
                        record = record_console.export_svg()
                    case "txt":
                        record = record_console.export_text()
                    case _:
                        record = False

                if record:
                    with open(f"construct_report.{report_type}", "wt") as report:
                        report.write(record)

        return success, failure


    def produce_extract_report(self, extractions: List[Dict], console):
        """
        Produce report of extractions list. Options are html, svg, txt, or console.

        ONLY FOR USE WITH CLI CLIENT
        """

        report_type = input(
            "\nHow would you like to process the extraction(s)?\nOutput will be sent to working directory named 'extract_report.[ext]' if a file.\nOptions: html, text, svg, console\nFor none press enter. "
        )
        match report_type.lower().strip():
            case "html":
                report_type = "html"
            case "svg":
                report_type = "svg"
            case "text":
                report_type = "text"
            case "console":
                report_type = "console"
            case _:
                report_type = None


        if report_type is not None:
            if report_type == "console":
                console.print('Extracted Info:', style="cyan")


                for extracted in extractions:
                    for key, value in extracted.items():
                        console.print(key, ':', value, style="success")
                    
                    console.print('\n')
            else:
                record_console = Console(record=True, stderr=True, file=StringIO())
                record_console.rule('Extracted Info:', style="cyan")

                for extracted in extractions:
                    for key, value in extracted.items():
                        record_console.print(key, ':', value, style="bold green")
                    
                    record_console.print('\n')
                record_console.rule(f"Report Generated {datetime.now().ctime()}")


                match report_type:
                    case "html":
                        record = record_console.export_html()
                    case "svg":
                        record = record_console.export_svg()
                    case "txt":
                        record = record_console.export_text()
                    case _:
                        record = False

                if record:
                    with open(f"extract_report.{report_type}", "wt") as report:
                        report.write(record)
        
        else:
            console.print("No report generated.", style="yellow")

    def get_all_artists(self) -> List[Dict]:
        """
        Returns a list of all artists in the database.
        """
        return self.database.get_all_artists()

    def get_artist_by_id(self, artist_id: int) -> List[Dict]:
        """
        Returns a list of all artists in the database.
        """
        return self.database.get_artist_by_id(artist_id)

    def get_all_artists_and_songs(self) -> Dict:
        """
        Returns a dict of all artists and their songs in the database.
        """
        songs = {}
        artists = self.database.get_all_artists()
        for artist in artists:
            songs[artist["name"]] = self.database.get_songs_by_artist_by_id(artist["artist_id"])
        return songs

    def get_songs_by_artist(self, artist_id: int) -> List[Dict]:
        """
        Returns a list of all songs by a given artist.
        """
        return self.database.get_songs_by_artist_by_id(artist_id)

    def get_song_by_id(self, song_id: int) -> Dict:
        """
        Returns a song with the given ID.
        """
        return self.database.get_song_by_id(song_id)

    def construct(self, constructor: str, data: List[Dict] = None, auto: bool = False) -> Dict:
        """
        Constructs new audio files from the data in the database and returns a dictionary containing the
        filenames and the options used to construct them.
        """
        data = data or self.current_data
        if constructor not in self.config.constructors:
            raise TypeError(f"constructor {constructor} does not exist")
        self.constructor = Constructor(data, constructor, auto)
        self.constructor.from_dict()
        return {
            "success": self.constructor.get_success(),
            "failure": self.constructor.get_failure()
        }
