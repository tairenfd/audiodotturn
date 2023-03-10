GENERAL USAGE
=============

::
    
    audiodotturn [-h] [-v] [-c CONFIG] [-D DATABASE] [--defaults [{program,format,all}]] [--options [{program,format,all}]] {set,create,view} ...

    Format, organize and retrieve data from audio files.

    positional arguments:
    {set,create,view}
        set                 Set defaults
        create              Create subcommands
        view                View subcommands

    options:
    -h, --help            show this help message and exit
    -v, --version         Show current version of audiodotturn
    -c CONFIG, --config CONFIG
                            Path to a specific configuration file to use for the session.
    -D DATABASE, --database DATABASE
                            Path to .db file for library database
    --defaults [{program,format,all}]
                            Show default settings
    --options [{program,format,all}]
                            Show default settings

SET COMMAND USAGE
-----------------

::

    audiodotturn set [-h] [-d] [-a ARTIST] [-t TITLE] [-f FEATURES] [-m MISC] [-y YOUTUBE_ID] [--filetype FILETYPE] [-s {true,false}] [-q DATA] [-p DIRECTORY]
                            [-x {default,standard,normal,yt,youtube}] [-b CONSTRUCTOR] [-e ERRORMSG] [--exts EXTS]

    options:
    -h, --help            show this help message and exit
    -d, --dry             Dry run

    formatting options:
    -a ARTIST, --artist ARTIST
                            Default artist name for audio files
    -t TITLE, --title TITLE
                            Default title for audio files
    -f FEATURES, --features FEATURES
                            Default features for audio files
    -m MISC, --misc MISC  Default miscellaneous info for audio files
    -y YOUTUBE_ID, --youtube-id YOUTUBE_ID
                            Default YouTube ID for audio files
    --filetype FILETYPE   Default audio file type

    program options:
    -s {true,false}, --dryset {true,false}
                            Default dry run setting
    -q DATA, --data DATA  Default JSON filename
    -p DIRECTORY, --path DIRECTORY
                            Default working directory
    -x {default,standard,normal,yt,youtube}, --extractor {default,standard,normal,yt,youtube}
                            Default extractor
    -b CONSTRUCTOR, --constructor CONSTRUCTOR
                            Default constructor
    -e ERRORMSG, --error ERRORMSG
                            Default error message options. comma seperated string of options.
    --exts EXTS           Default formattable file extensions. comma seperated string of options.

CREATE COMMAND USAGE
--------------------

::

    audiodotturn create [-h] [-f FORMAT] [-x EXTRACTOR] [-b CONSTRUCTOR] [-F] [-o] [--dry] [-p DIRECTORY]

    options:
    -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
                            Format single file
    -x EXTRACTOR, --extractor EXTRACTOR
                            Define the extractor to use
    -b CONSTRUCTOR, --constructor CONSTRUCTOR
                            Define the constructor to use
    -F, --formatdir       Format all files in directory
    -o, --organize        Organize all files in directory and create database entries if they dont exist.
    --dry                 Dry run
    -p DIRECTORY, --path DIRECTORY
                            Directory to organize or format files, the programs working directory

VIEW COMMAND USAGE
------------------

::

    audiodotturn view [-h] {artists,songs} ...

    positional arguments:
    {artists,songs}
        artists        View list of artists
        songs          View list of songs

    options:
    -h, --help       show this help message and exit
