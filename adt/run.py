"""
Basically used for all print handling
"""
import os
from rich.console import Console
from rich.theme import Theme
from rich.progress import track
from adt import VERSION
from adt import AudioDotTurn
from adt.parser import Parser


def init():
    """
    Initialize AudioDotTurn.

    Returns:
        tuple:
            args (parser.parse_args()),
            adt (AudioDotTurn)
    """
    parser = Parser()
    args = parser.parse_args()
    config_path = args.cfgpath or None
    db_path = args.dbpath or None
    adt = AudioDotTurn(config_path=config_path, db_path=db_path)

    return args, adt

def rich_inits():
    #rich initialisations
    theme = Theme(
        {
            "success": "bold green",
            "failure": "magenta",
            "error": "bold red",
            "info": "bold yellow"
        }
    )
    console = Console(theme=theme)

    return console

def extract_commands(args, adt: AudioDotTurn):
    """
    Extracts information from a given file or multiple files.

    Args:
        args (Namespace): Command line arguments.
        adt (AudioDotTurn): AudioDotTurn instance.
    """
    console = rich_inits()
    opt = args.out
    success = 0
    failure = 0

    if args.file:
        extraction = adt.extract_file(args.file, opt)[0]
        console.print(extraction, '\n', style="info")

    elif args.multi:
        extractions = adt.extract_files(args.multi, opt)
        adt.produce_extract_report(extractions, console)
        for extracted in extractions:
            if extracted["status"]:
                success += 1
            else:
                failure += 1
        console.print(f"\nsuccess: {success}\nfailure: {failure}")

    elif args.dir:
        try:
            files = [file for file in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, file)) and file.endswith(tuple(adt.config.exts))]
        except NotADirectoryError as error:
            console.print(error)
            return

        extractions = adt.extract_files(files, opt)
        adt.produce_extract_report(extractions, console)
        for extracted in extractions:
            if extracted["status"]:
                success += 1
            else:
                failure += 1
        console.print(f"\nsuccess: {success}\nfailure: {failure}")


def construct_commands(args, adt: AudioDotTurn):
    """
    Constructs an output file from a given file or multiple files.

    Args:
        args (Namespace): Command line arguments.
        adt (AudioDotTurn): AudioDotTurn instance.
    """
    console = rich_inits()
    constructor_type = args.constructor
    success = 0
    failure = 0

    if args.file:
        extraction = adt.extract_file(args.file)
    elif args.multi:
        extraction = adt.extract_files(args.multi)
        adt.produce_extract_report(extraction, console)
    elif args.dir:
        extraction = adt.extract_file([file for file in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, file)) and file.endswith(tuple(adt.config.exts))])
        adt.produce_extract_report(extraction, console)

    if not any((args.file, args.multi)):
        return

    results = adt.construct(constructor_type, extraction, args.auto)

    success, failure = adt.produce_construct_report(results, console, args)

    if success == 0 and failure == 0:
        console.print("\n[bold red]Run aborted.")
    else:
        console.print(f"\nsuccess: {success}\nfailure: {failure}")


def database_commands(args, adt: AudioDotTurn):
    """
    Manipulates the database.

    Args:
        args (Namespace): Command line arguments.
        adt (AudioDotTurn): AudioDotTurn instance.
    """
    console = rich_inits()

    if args.updatefile:

        console.print(f"Current database in use or to be created is {os.path.abspath(adt.config.db_path)}\n")
        confirm = input("continue? [y/N]")
        if confirm.lower() not in ['yes', 'y', 'yy']:
            console.print("Exiting\n", style="error")
            return

        extraction = adt.extract_file(args.updatefile)

        console.print('Extracted Info:', style="cyan")
        for key, value in extraction[0].items():
            console.print(key, ':', value, style="success")
        console.print('\n')

        confirm = input("update database [y/N]: ")
        if confirm.lower() not in ['yes', 'y', 'yy']:
            console.print("Exiting\n", style="error")
            return

        new_artists, new_songs, updated, failure = adt.update_database(extraction)
        if new_artists:
            console.print("New artist successfully added\n")
        if new_songs:
            console.print("New song successfully added\n")
        if updated:
            console.print("Entry updated successfully\n")
        if failure:
            console.print("Update failed\n")
    
    elif args.updatemulti:

        console.print(f"Current database in use or to be created is {os.path.abspath(adt.config.db_path)}\n", style="cyan")
        confirm = input("continue? [y/N]")
        if confirm.lower() not in ['yes', 'y', 'yy']:
            console.print("Exiting\n", style="error")
            return

        confirm_print = input("\nExamine extraction results before updating? [y/N]")
        if confirm_print.lower() not in ['yes', 'y', 'yy']:
            console.print("Exiting\n", style="error")
            return

        extractions = adt.extract_files(args.updatemulti)

        adt.produce_report(extractions, console)
                
        confirm = input("update database [y/N]: ")
        if confirm.lower() not in ['yes', 'y', 'yy']:
            console.print("Exiting\n", style="error")
            return

        new_artists, new_songs, updated, failure = adt.update_database(extractions)
        console.print(
            f"New artists: {new_artists}",
            f"New songs: {new_songs}\n",
            f"Updated: {updated}",
            f"Failure: {failure}\n"
        )

    elif args.artists:
        artists = adt.get_all_artists()
        if artists:
            for artist in track(artists, "Fetching artists..."):
                console.print(f'id: {artist["artist_id"]}, name: {artist["name"]}')
        else:
            console.print('None found.\n', style="info")

    elif args.songs:
        songs = adt.get_all_artists_and_songs()
        if songs:
            for artist, songs in track(songs.items(), "Fetching tracks..."):
                console.print(artist, style="success")
                for _id, song in enumerate(songs, start=1):
                    console.print(str(song).strip('{}'))
        else:
            console.print('None found.\n', style="info")

    elif args.artistid:
        songs = adt.get_songs_by_artist(args.artistid)
        if songs:
            for song in track(songs, "Fetching tracks..."):
                console.print(song, style="success")
        else:
            console.print('None found.\n', style="info")

    elif args.songid:
        song = adt.get_song_by_id(args.songid)
        if song:
            console.print(song, style="success")
        else:
            console.print("None found.\n", style="info")


def main():
    """
    Main function.
    """
    try:
        args, adt = init()
        console = rich_inits()

        if args.version:
            console.print(adt.config.app_name, VERSION, style="cyan")

        if args.settings:
            settings = {
                "audiodoturn": VERSION,
                "config path": adt.config.config_path,
                "db path": adt.config.db_path,
                "constructors": adt.config.constructors,
                "exts": adt.config.exts,
                "output options": adt.config.output_opts,
                "dry run": adt.config.dry
            }

            for key, value in settings.items():
                console.print(key, ':', value)
        
        if args.command == "extract":
            extract_commands(args, adt)

        elif args.command == "construct":
            construct_commands(args, adt)

        elif args.command == "database":
            database_commands(args, adt)

    except Exception:
        console.print_exception()

if __name__ == "__main__":
    main()
