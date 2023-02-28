# AudioDotTurn

AudioDotTurn is a tool designed to help format and organize files that have been downloaded using yt-dlp without properly formatted file names or metadata.  
The tool allows users to format titles, organize tracks into artist directories and a JSON dataset of the songs to help with organizing and searching for specific songs or artists. 


## Installation

To use AudioDotTurn, follow these steps:

1. Clone the AudioDotTurn repository to your local machine.
2. Run the program using `python AudioDotTurn.py`.


## Dependencies

External libraries:
 - rich (pip install rich or check out [rich](https://github.com/Textualize/rich))

Standard:
 - os
 - re
 - json
 - argparse
 - shutil


## File formatting examples

Default format output 

        [{artist}][{title}][{features}][{misc}][{youtube_id}].{filetype}

As of right now the file really just needs to end in ' [youtubeid].filetype' and it should be able to format it to an extent.

        AudioDotTurn.py create --formatfile 'YG Feat. Dj Mustard "Pop It, Shake It" (Uncut) (WSHH Exclusive - Official Music Video) [kQ2KSPz4iSw].wav' -> 
              [YG][Pop It, Shake It][Dj Mustard][Uncut, WSHH Exclusive - Official Music Video][kQ2KSPz4iSw].wav
              
        AudioDotTurn.py create --formatfile 'The Weeknd - Blinding Lights (Lyrics) [4NRXx6U8ABQ].mp3' -> 
              [The Weeknd][Blinding Lights][UNKNOWN][Lyrics][4NRXx6U8ABQ].mp3
              
        AudioDotTurn.py create --formatfile 'Lady Gaga, Ariana Grande - Rain On Me (Official Music Video) [AOm9Fv8NTG0].mp3' -> 
              [Lady Gaga, Ariana Grande][Rain On Me][UNKNOWN][Official Music Video][AOm9Fv8NTG0].mp3

        AudioDotTurn.py create --formatfile 'Music for Sleeping and Deep Relaxation: Delta Waves [HU3ZGMaVZj0].mp4' -> 
              [Music for Sleeping and Deep Relaxation][Delta Waves][UNKNOWN][UNKNOWN][HU3ZGMaVZj0].mp4

        AudioDotTurn.py create --formatfile 'Music [HU3ZGMaVZj0].mp4' -> 
              [Music][UNKNOWN][UNKNOWN][UNKNOWN][HU3ZGMaVZj0].mp4

If these 5 files were formatted with --dirs after filename formatting, it would create directories based off of the unique artist names- 'YG', 'The Weeknd', 'Lady Gaga, Ariana Grande', 'Music for Sleeping and Deep Relaxation' and 'Music' 
in this case - each containing the songs of the artist.

It usually handles trickier filenames okay too (still needs to end in ' [youtubeid].filetype')

        AudioDotTurn.py create --formatfile 'Zacari (adasdasdasd) ft. Isaiah Rashad [misc misc] - Bliss (Official Audio) [audio] [9o1gLWxHI7Q].mp3'i ->
              [Zacari][Bliss][Isaiah Rashad][adasdasdasd, Official Audio, misc misc, audio][9o1gLWxHI7Q].mp3 

        AudioDotTurn.py create --formatfile 'ZillaKami x SosMula ＂33rd Blakk Glass＂(WSHH Exclusive - testing) [9o1gLWxHI7Q].mp3'
              [ZillaKami x SosMula][33rd Blakk Glass][UNKNOWN][WSHH Exclusive - testing][9o1gLWxHI7Q].mp3 


## More Info

Some images and more info about the program can be found at [tairenfd.xyz](https://tairenfd.xyz/projects/mp3-formatter)

## Usage

AudioDotTurn has two main commands: `create` and `view`. 

The `create` command allows you to format and/or organize your files, while the `view` command allows you to view information about your existing data.

### Flags and positional arguments

      usage: AudioDotTurn.py [-h] {create,view} ...

      Format, orgranize and retrieve data from files in an audio library.

      positional arguments:
        {create,view}  commands
          create       Create subcommands
          view         View subcommands

      optional arguments:
        --defaults     show default settings
        -h, --help     show this help message and exit

      Create subcommands:
        -d, --dirs          Organize files in artist directories
        -f, --formatfile    Format single file
        -F, --formatdir     Format all files in directory
        -D, --dump          Dump directory into JSON file
        --filename FILENAME Name of JSON file
        --dry               Dry run
        --directory DIR     Directory to organize or format files

      View subcommands:
        -d DATA             JSON data to view

      View Artists:
        artists             View list of artists
          -t, --tracks      View list of artists and their tracks
          -n, --names       View list of artist names

      View Songs:
        songs               View list of songs
          -a ARTIST         View list of songs by artist
          -i ID             View list of songs by ID
          -N NAME           View list of songs by name

### Creating a dataset

To create a dataset, you first need to format your filenames. There are three options for formatting filenames:

1. **Format a single file:** 

        `python AudioDotTurn.py create --formatfile [filename]`

   This will format the filename using the default format. The default format is:

        -> [{artist}][{title}][{features}][{misc}][{youtube_id}].{filetype}

   If your file doesn't follow this format, the tool will attempt to format it as best it can. You can also specify a custom format using the `--format` option.

2. **Format all files in a directory:**

        `python AudioDotTurn.py create --formatdir [directory]`

   This will format all files in the specified directory using the default format.

3. **Organize files into artist directories:**

        `python AudioDotTurn.py create --dirs [directory]`

   This will organize all files in the specified directory into artist directories based on the artist names in the filenames.

After formatting your filenames, you can create a dataset using the `--dump` option:

        `python AudioDotTurn.py create --dump --filename [filename] [directory]`

This will create a JSON file with information about your formatted files.

### Viewing information

To view information about your dataset, you can use the `view` command. There are two options for viewing information:

1. **View a list of artists:**

        `python AudioDotTurn.py view --data [datafile] artists --names`

   This will display a list of all artists in the dataset.

        `python AudioDotTurn.py view --data [datafile] artists --tracks`

   This will display a list of all artists in the dataset along with their tracks.

2. **View a list of songs:**

        `python AudioDotTurn.py view --data [datafile] songs --artist [artist name]`

   This will display a list of all songs by the specified artist.

        `python AudioDotTurn.py view --data [datafile] songs --id [youtube ID]`

   This will display a list of all songs with the specified youtube ID.

        `python AudioDotTurn.py view --data [datafile] songs --name [track name]`

   This will display a list of all songs with the specified track name.


### Example dataset

      {
        "Koly P": {
          "tracks": [
            {
              "title": "Rapture Of Thugs",
              "features": "Polo pooh",
              "misc": "KOLYON",
              "youtube_id": "xZEK6luuZ2k",
              "filetype": "mp3"
            },
            {
              "title": "Walk Down",
              "features": "UNKNOWN",
              "misc": " Official Video ",
              "youtube_id": "sJzTb7skSKM",
              "filetype": "mp3"
            }
          ]
        },
        "Isaiah Rashad": {
          "tracks": [
            {
              "title": "All Herb",
              "features": "Amindi",
              "misc": "UNKNOWN",
              "youtube_id": "NpcsssBx2Y0",
              "filetype": "mp3"
            },
            {
              "title": "The Race Freestyle",
              "features": "UNKNOWN",
              "misc": "Tay-K",
              "youtube_id": "Rf4S_44jkAY",
              "filetype": "mp3"
            }
          ]
        }
      }

## Roadmap

 - Remove [youtube_id] dependency
 - Allow to confirm/deny filename changes
 - General regex adjusting for broader use
 - Refactoring code for better readability and maintainability
 - Bug fixes and optimization


## License

This project is licensed under the MIT License. See the LICENSE file for more information.
