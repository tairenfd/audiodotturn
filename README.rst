audiodotturn 0.4.0
==================

.. image:: https://img.shields.io/pypi/v/audiodotturn.svg
    :target: https://pypi.org/project/audiodotturn/

AudioDotTurn is a tool for formatting and organizing audio files with little to no metadata available. It provides a solution
for situations where there are tons of unstandardized, unorganized files with little to no metadata, and sorting via metadata
is not an option. With AudioDotTurn, users can quickly format a single file or a whole directory/subdirectories to the style of
their choosing. 

The tool creates a database for the user, which can be accessed via AudioDotTurn or any program that will interpret sql .db files.
The database will be updated as new files are formatted as long as the db file is selected as the default db or selected at runtime.

- Users can change settings via CLI
- AudioDotTurn uses pretty output via rich for visually appealing output
- Dry run mode available for seeing results of a run without making any actual changes
- When formatting an entire directory, users can produce a report of the results in an MD file or simply print them to the console if either are desired.

Set User Config
===============

Depending on how your system and python PATHs are set the installation path may differ.
Usually however, you should be able to find the default config.json in one of the below

 .. code:: sh

    /home/user/.local/lib/python{3}.{11}/site-packages/audiodotturn/config/config.json
    /usr/local/lib/python{x}.{x}/site-packages/audiodotturn/config/config.json
    /usr/lib/python{x}.{x}/site-packages/audiodotturn/config/config.json

Once the default config is found, copy it to one of the below paths with `cp <DEFAULT_CONFIG> <NEW_PATH>`

.. code:: sh

    ~/.config/audiodotturn/
    ~/config/audiodotturn/
    ~/audiodotturn/
    ~/
    /usr/local/etc/audiodotturn/
    /etc/audiodotturn/

Once copied rename the config file to adt_config.json and change any desired settings, if the config warning is no longer showing up,
then your new config has loaded properly.

A config can also be set at runtime with the `-c` flag

Dependencies
============

External libraries: 

	- `rich <https://github.com/Textualize/rich>`__

Standard: 

	- os 
	- re 
	- json 
	- argparse 
	- shutil

Choosing a formatter
====================

TODO

Currently standard formatter will always be ran. It should format most files fairly well.

Choosing a constructor
======================

TODO: explain

- "simple":
- "block":

Creating a database
===================

Database path is set in config or during runtime.

A new database will be created if one isnt already when running the create or view commands.
Populate the database by using the format file or format directory commands, this will update
a database as well. I recommend doing this with dry run if you just want to create a database
without formatting any files.

.. include:: USAGE.rst

.. include:: EXAMPLES.rst

Disclaimer
==========

AudioDotTurn is currently in alpha testing and is provided as is with no
warranties or guarantees of any kind. The author of the program is not
responsible for any damages or issues caused by the use of this program.
Use at your own risk.

Roadmap
=======

-  General regex adjusting for broader use
-  Bug fixes and optimization

License
=======

.. figure:: https://img.shields.io/badge/License-MIT-yellow.svg
   :alt: MIT

This project is licensed under the MIT License. See the LICENSE file for
