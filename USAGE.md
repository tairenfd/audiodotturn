GENERAL
=======

```sh
    usage: adt [-h] [-v] [-p CFGPATH] [-d DBPATH] [-s] {extract,construct,database} ...

    Format, organize and retrieve data from audio files.

    positional arguments:
    {extract,construct,database}
        extract             Extraction commands
        construct           Construction commands
        database            Database commands

    options:
    -h, --help            show this help message and exit
    -v, --version         Show current version of audiodotturn
    -p CFGPATH, --cfgpath CFGPATH
                            Path to a specific configuration file to use for the session.
    -d DBPATH, --dbpath DBPATH
                            Path to .db file for library database
    -s, --settings        Show current settings
```

EXTRACT
=======

```sh
    usage: adt extract [-h] [-o OUT] [-f FILE] [-m MULTI [MULTI ...]] [-l DIR]

    options:
    -h, --help            show this help message and exit
    -o OUT, --out OUT     Output format for extraction, default is dict.
    -f FILE, --file FILE  Extract info from single file.
    -m MULTI [MULTI ...], --multi MULTI [MULTI ...]
                            Extract info from multiple files.
    -l DIR, --dir DIR     Extract info from files in a directory.
```

CONSTRUCT
=========

```sh
    usage: adt construct [-h] [-a] [-c CONSTRUCTOR] [-f FILE] [-m MULTI [MULTI ...]]

    options:
    -h, --help            show this help message and exit
    -a, --auto            Set auto-choice
    -c CONSTRUCTOR, --constructor CONSTRUCTOR
                            Constructor to use
    -f FILE, --file FILE  Construct from a single file
    -m MULTI [MULTI ...], --multi MULTI [MULTI ...]
                            Construct from multiple files
```

DATABASE
========

```sh
    usage: adt database [-h] [-f UPDATEFILE] [-m UPDATEMULTI [UPDATEMULTI ...]] [-A] [-S] [-Ai ARTISTID] [-Si SONGID]

    options:
    -h, --help            show this help message and exit
    -f UPDATEFILE, --updatefile UPDATEFILE
                            Update database via file.
    -m UPDATEMULTI [UPDATEMULTI ...], --updatemulti UPDATEMULTI [UPDATEMULTI ...]
                            Update database via multiple files.
    -A, --artists         View all artists within the database
    -S, --songs           View all songs by each artist within the database
    -Ai ARTISTID, --artistid ARTISTID
                            View songs by artist id
    -Si SONGID, --songid SONGID
                            View song by song id
```
