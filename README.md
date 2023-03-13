audiodotturn 0.5.3
==================

General tool/library for extracting simple metadata and producing new file formats from only a filename(s).

Metadata can be catalogued and viewed via a sql database created by audiodotturn

Extraction and construction reports can be generated in multiple file formats. 

INSTALLATION
============

```sh
    pip install audiodotturn
```

CONFIGURATION
=============

User configuration settings can be set in a config.ini file placed in one of the following locations

- ~/.config/audiodotturn/config.ini,
- ~/config/audiodotturn/config.ini,
- ~/audiodotturn/config.ini,
- ~/.audiodotturn/config.ini,

User Configuration options shown below

```ini
    [DATABASE]
    path = <DATABASE PATH>

    [PROGRAM]
    exts = <COMMA SEPERATED LIST OF EXTS ie. .mp3, .mp4, .wav>
    dry = <True/False>
```

To make sure the config settings are loaded correctly you can run `adt -s` to get an overview of the current settings being used

Dependencies
============

External libraries: 

- [rich](https://github.com/Textualize/rich)
- [pyyaml](https://github.com/yaml/pyyaml)

Standard: 

- os
- typing
- datetime
- sqlite3
- re 
- json 
- argparse 
- shutil

USAGE
=====

The extract, construct, and database modules are non-dependent on any other part of the program

Rich is only neccessary for use with the adt module or run module. The run module will soon be 
non-dependent on rich. It is only used for better user experience.

Refer to [USAGE](./USAGE.md)

EXAMPLES
========

Refer to [EXAMPLES](./EXAMPLES.md)

Choosing a constructor
======================

- "simple":
    This will produce several file options formatted as a standard audio track ie. Artist - Title ft. Feat (etc etc).mp3
- "enclosed":
    This will produce several file options formatted as an enclosed file name ie. (Artist)(Title)(Feat)(etc)(yt-id).mp3

Creating a database
===================

Database path is set in config or during runtime.

A new database will be created upon the first database update.

Increased database funcitonality can be obtained through importing `adt` as a library.
See examples in [EXAMPLES](./EXAMPLES.md)

License
=======

![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License. See the LICENSE file for more info.
