EXAMPLES
========

Setting default options
-----------------------

The below command is a run through of the `set` command during a dry run.

::

    $ audiodotturn set --dry -a "N/A" -t "No Title" --dryset true

    ->  Enter editor for format defaults?
        [y/n]: 

    ->  Changes being made to:                     
            artist -> UNKNOWN to                       
            N/A                                        
                                                        

        Are you sure you want to make these changes? 
        [y/n]:

    ->  repeat previous for all format defaults being changed

    ->                       Confirmed                          
                        change: title = No Title.                                     
                                                                    
                        File updated at {config path will show here}                          
                ╭───────────────────── Modified ─────────────────────╮
                │ title changed to No Title                          │
                ╰────────────────────────────────────────────────────╯
                ╭──────────────────── Cancelled ─────────────────────╮
                │ artist will remain as UNKNOWN                      │
                ╰────────────────────────────────────────────────────╯
                ╭─────── Hypothetical New Formatting Section ────────╮
                │ {                                                  │
                │   "artist": "UNKNOWN",                             │
                │   "title": "No Title",                             │
                │   "features": "UNKNOWN",                           │
                │   "misc": "UNKNOWN",                               │
                │   "youtube_id": "UNKNOWN",                         │
                │   "filetype": "mp3"                                │
                │ }                                                  │
                ╰────────────────────────────────────────────────────╯

    ->  Enter editor for program defaults?
        [y/n]:

    ->  Process is repeated for program defaults if any were chosen, in this case it would confirm changes to the dry run setting. 


Formatting a single file
------------------------

This example will be ran in dry mode

::

    $ audiodotturn create --dry -f 'turn (ft. tester) "long john" ft. me, turner.wav'

    ->  Construction successful! You're in dry run mode, would
        you like to update the database anyways?
        [y/n]: 

We'll go with no for this run

::

    ->  options = 

        - 1    Turn - long john.wav

        - 2    Turn - long john ft. tester, me, turner.wav

        - 3    Turn - long john ft. tester, me, turner 
        (UNKNOWN).wav

Lets go with option 2

::

    ->  Which would you like to use?: 2
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃               RESULT STATUS: SUCCESS               ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                            DRY_RUN                        

        OLD: turn (ft. tester) "long john" ft. me, turner.wav 

        NEW: Turn - long john ft. tester, me, turner.wav 


Format all files in a directory in a particular style
-----------------------------------------------------

::

    $ audiodotturn create --dry -b block -F -p ../test-songs/

    ->  Dry mode is currently: true
        Would you like to create database entries? This must 
        be confirmed regardless of dry run status. [y/n]: 

When using the `create` or `view` commands an empty database is always created in the default working directory if 
it doesnt exist unless a database is passed in. 

In this example I will choose 'n'

::

    ->  Create a file listing the changes in ../test-songs/ or
        view them in the console, or neither? (Short summary 
        of change stats will be shown upon completion 
        regardless)
        [file/console/none]: 

If you want to view all the chnages that would have been made you can create a readme containing the info in the 
currently set working directory/path set with `-p`, view it in the console, or simply just get the short summary with 'none'.

We'll check out the short summary.

::

    ->    [04:28:00] DRY RUN: true               cli.py:159
                Changed: 3                       cli.py:160
                Unchanged: 9                     cli.py:161
                Error Formatting: 2              cli.py:162

In this instance there were already 9 files formatted as the `block` style, and 3 files which needed to be formatted and were successfully.
Typically errors are non-audio files. In this case its a readme and a json file that happen to be in that directory. You can get this info
through the more verbose summaries.


Viewing
-------

.. note::
    This will be visually updated soon
    Also, all searches look for substrings and not literals


**list of artists**

::

    $ audiodotturn view artists -N

    ->  ['koly p', 'zacari', 'zillakami x sosmula', 'isaiah rashad']

**list of songs by an artist**

::

        $ audiodotturn view songs -A "koly"

    ->  [
            {
                'artist': 'koly p',
                'title': '06',
                'features': 'unknown',
                'misc': 'wshh exclusive - official music 
                    video',
                'youtube_id': '-Qy_YaqMzAo',
                'filetype': 'mp3'
            }
        ]

**view tracks by artist**

::

    ->  [
            {
                'artist': 'zacari',
                'title': 'bliss',
                'features': 'isaiah rashad',
                'misc': 'adasdasdasd, official audio',
                'youtube_id': '9o1gLWxHI7Q',
                'filetype': 'mp3'
            }
        ]
