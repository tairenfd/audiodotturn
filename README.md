# AudioDotTurn

If you're tired of your audio files being a complete mess with poorly formatted names and missing metadata this might be your solution.  

Using audiodotturn you can quickly and easily organize your entire audio library with just a few commands.

## Table of Contents

- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
  - [Flags and positional arguments](#flags-and-positional-arguments)
  - [Choosing a formatter](#choosing-a-formatter)
  - [Creating a dataset](#creating-a-dataset)
  - [Viewing information](#viewing-information)
- [Examples](#examples)
  - [File formatting examples](#file-formatting-examples)
  - [Example dataset](#example-dataset)
- [Disclaimer](#disclaimer)
- [Roadmap](#roadmap)
- [License](#license)


## Installation

```sh
  pip install git+https://github.com/tairenfd/audiodotturn.git
```
or
```sh
  git clone https:github.com/tairenfd/audiodotturn.git
  pip install ./ 
```  
or run without installing with 
```sh
  python audiodotturn
```
after cloning the repo


## Dependencies

External libraries:
 - [rich](https://github.com/Textualize/rich)

Standard:
 - os
 - re
 - json
 - argparse
 - shutil


## Usage

AudioDotTurn has two main commands: `create` and `view`. 

The `create` command allows you to format and/or organize your files, while the `view` command allows you to view information about your existing data.

### Flags and positional arguments

```sh
    usage: AudioDotTurn.py [-h] {create,view} ...

    Format, orgranize and retrieve data from files in an audio library.

    positional arguments:
      {create,view}  commands
        create       Create subcommands
        view         View subcommands

    optional arguments:
      --defaults                            Show default settings
      --defaults [{settings,options,all}]   Show default settings
      -h, --help                            Show this help message and exit

      Create subcommands:
        -d, --dirs                    Organize files in artist directories
        -x. --formatter  FORMATTER    Define the formatter to use
        -f, --formatfile FORMATFILE   Format single file
        -F, --formatdir               Format all files in directory
        -D, --dump                    Dump directory into JSON file
        --filename FILENAME           Name of JSON file
        --directory DIR               Directory to organize or format files
        --dry                         Dry run

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
```

### Choosing a formatter

The default formatter is now the 'standard' formatter which applies no youtube_id data attribute but otherwise works the same. It will still read formatted files with a youtube_id fine when creating a json, but will not create new datasets with youtube_id's - instead putting that info if provided into the 'misc' category. This is the recommended formatter for general use.

The 'youtube' formatter is primarily for files downloaded with yt-dlp that still contain a suffix of [youtube_id].ext

You can set a default formatter in the config.json file, or set it during runtime with `-x [formatter]`

To view the currently set default formatter use `audiodotturn --default settings` - default formatter listed under `program_defaults -> formatter`  

You can view the available formatters with `audiodotturn --defaults options` - options will be under `formatter`

### Creating a dataset

To create a dataset, you first need to format your filenames. There are three options for formatting filenames:

1. **Format a single file:** 

```sh
      audiodotturn create --formatfile [filename]
```

   This will format the filename using the default format.

   If your file doesn't follow this format, the tool will attempt to format it as best it can. You can also specify a custom format using the `--format` option.

2. **Format all files in a directory:**

```sh
      audiodotturn create --formatdir [directory]
```

   This will format all files in the specified directory using the default format.

3. **Organize files into artist directories:**

```sh
      audiodotturn create --dirs [directory]
```

   This will organize all files in the specified directory into artist directories based on the artist names in the filenames.

After formatting your filenames, you can create a dataset using the `--dump` option:

```sh
      audiodotturn create --dump --filename [filename] [directory]
```

This will create a JSON file with information about your formatted files.

### Viewing information

To view information about your dataset, you can use the `view` command. There are two options for viewing information:

1. **View a list of artists:**

```sh
      audiodotturn view --data [datafile] artists --names
```

   This will display a list of all artists in the dataset.

```sh
      audiodotturn view --data [datafile] artists --tracks
```

   This will display a list of all artists in the dataset along with their tracks.

2. **View a list of songs:**

```sh
      audiodotturn view --data [datafile] songs --artist [artist name]
```

   This will display a list of all songs by the specified artist.

```sh
      audiodotturn view --data [datafile] songs --id [youtube ID]
```

   This will display a list of all songs with the specified youtube ID.

```sh
      audiodotturn view --data [datafile] songs --name [track name]
```

   This will display a list of all songs with the specified track name.


## Examples

### File formatting examples

* Note: The below are only examples using the 'youtube' formatter. More examples will be added soon.

- `[YG Feat. Dj Mustard "Pop It, Shake It" (Uncut) (WSHH Exclusive - Official Music Video) [kQ2KSPz4iSw].wav]` formats as `[YG][Pop It, Shake It][Dj Mustard][Uncut, WSHH Exclusive - Official Music Video][kQ2KSPz4iSw].wav`
- `[The Weeknd - Blinding Lights (Lyrics) [4NRXx6U8ABQ].mp3]` formats as `[The Weeknd][Blinding Lights][UNKNOWN][Lyrics][4NRXx6U8ABQ].mp3`
- `[Lady Gaga, Ariana Grande - Rain On Me (Official Music Video) [AOm9Fv8NTG0].mp3]` formats as `[Lady Gaga, Ariana Grande][Rain On Me][UNKNOWN][Official Music Video][AOm9Fv8NTG0].mp3`
- `[Music for Sleeping and Deep Relaxation: Delta Waves [HU3ZGMaVZj0].mp4]` formats as `[Music for Sleeping and Deep Relaxation][Delta Waves][UNKNOWN][UNKNOWN][HU3ZGMaVZj0].mp4`
- `[Music [HU3ZGMaVZj0].mp4]` formats as `[Music][UNKNOWN][UNKNOWN][UNKNOWN][HU3ZGMaVZj0].mp4`

- `Zacari (adasdasdasd) ft. Isaiah Rashad [misc misc] - Bliss (Official Audio) [audio] [9o1gLWxHI7Q].mp3` formats as `[Zacari][Bliss][Isaiah Rashad][adasdasdasd, Official Audio, misc misc, audio][9o1gLWxHI7Q].mp3`  

- `ZillaKami x SosMula ＂33rd Blakk Glass＂(WSHH Exclusive - testing) [9o1gLWxHI7Q].mp3` formats as `[ZillaKami x SosMula][33rd Blakk Glass][UNKNOWN][WSHH Exclusive - testing][9o1gLWxHI7Q].mp3`

### Example dataset

```json
  {
    "Koly P": {
      "tracks": [
        {
          "title": "Rapture Of Thugs",
          "features": "Polo pooh",
          "misc": "KOLYON",
          "youtube_id": "xZEK6luuZ2k",
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
```

## Disclaimer

AudioDotTurn is currently in alpha testing and is provided as is with no warranties or guarantees of any kind. The author of the program is not responsible for any damages or issues caused by the use of this program. Use at your own risk.


## Roadmap

 - Remove [youtube_id] dependency
 - Allow to confirm/deny filename changes
 - General regex adjusting for broader use
 - Refactoring code for better readability and maintainability
 - Bug fixes and optimization


## License

![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License. See the LICENSE file for more information.
