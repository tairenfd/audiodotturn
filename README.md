# MP3-PY

MP3-PY is a tool designed to help organize MP3 files that have been downloaded using yt-dlp without properly formatted file names or metadata. The tool allows users to create artist directories and a JSON dataset of MP3 files to help with organizing and searching for specific songs or artists. 

## Installation

To use MP3-PY, follow these steps:

1. Clone the MP3-PY repository to your local machine.
3. Run the program using `python mp3-py.py`.

### Dependencies
 - os
 - re
 - json
 - argparse
 - shutil
 - rich

## Usage

The MP3-PY tool includes two main commands: `create` and `view`.

### Create Sub-Command
The create sub-command has three optional arguments: --dirs, --formatfile, and --formatdir. These are used to process formatted MP3 files from a directory into artist directories and to format MP3 filenames according to a specific pattern.
              `
                python mp3-py.py create --dirs DIRECTORY
                python mp3-py.py create --formatfile FILENAME
                python mp3-py.py create --formatdir DIRECTORY
              `
### View Sub-Command
The view sub-command has three sub-commands: json, artists, and songs. The json sub-command has one optional argument: --dump, which is used to create a JSON of formatted MP3 files in a specified directory. The artists sub-command has two optional arguments: --tracks to list all artists in the dataset and their tracks, and --names to list all artists in the dataset. The songs sub-command has three optional arguments: --artist to specify the artist to display songs for, --id to search for a song by YouTube ID, and --name to search for a song by track title.
              `
                python mp3-py.py view --data DATASET json --dump DIRECTORY
                python mp3-py.py view --data DATASET artists --tracks
                python mp3-py.py view --data DATASET artists --names
                python mp3-py.py view --data DATASET songs --artist ARTIST
                python mp3-py.py view --data DATASET songs --id YOUTUBE_ID
                python mp3-py.py view --data DATASET songs --name TRACK_TITLE
              `
### MP3Create class
The MP3Create class has three methods: dirs(), format_file(), and format_files_dir(). The dirs() method is used to process formatted MP3 files from a directory into artist directories. The format_file() method is used to format an MP3 filename according to a specific pattern. The format_files_dir() method is used to format MP3 filenames in a specified directory according to a specific pattern.

### MP3View class
The MP3View class has six methods: json_dump(), get_artists(), get_artists_tracks(), get_songs_by_artist(), get_songs_by_id(), and get_songs_by_name(). The json_dump() method is used to create a JSON of the dataset. The other methods are used to query the dataset and return the results in Markdown format.

### Example dataset

      {
        "Koly P": {
          "tracks": [
            {
              "title": "\uff02Rapture Of Thugs\uff02",
              "features": "Polo pooh",
              "misc": "KOLYON",
              "video_id": "xZEK6luuZ2k",
              "filetype": "mp3"
            },
            {
              "title": "Walk Down",
              "features": "UNKNOWN",
              "misc": " Official Video ",
              "video_id": "sJzTb7skSKM",
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
              "video_id": "Audio] [NpcsssBx2Y0",
              "filetype": "mp3"
            },
            {
              "title": "The Race Freestyle",
              "features": "UNKNOWN",
              "misc": "Tay-K",
              "video_id": "Rf4S_44jkAY",
              "filetype": "mp3"
            }
          ]
        }
      }

## Roadmap
 - Fix WSHH regex filtering in titles
 - General regex adjusting for broader use
 - Refactoring code for better readability and maintainability
 - Bug fixes and optimization

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
