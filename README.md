audiodotturn
============

General tool/library for extracting simple metadata and producing new file formats from only a filename(s).

Metadata can be catalogued and viewed via a sql database created by audiodotturn

Extraction and construction reports can be generated in multiple file formats. 

INSTALLATION
------------

```sh
    pip install audiodotturn
```



CONFIGURATION
-------------

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

USAGE
-----

Refer to USAGE.md

EXAMPLES
--------

ROADMAP
-------

LICENSE
-------
