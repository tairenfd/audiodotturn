# MP3-PY

MP3-PY is a tool designed to help organize MP3 files that have been downloaded using yt-dlp without properly formatted file names or metadata. The tool allows users to create artist directories and a JSON dataset of MP3 files to help with organizing and searching for specific songs or artists. 


## Installation

To use MP3-PY, follow these steps:

1. Clone the MP3-PY repository to your local machine.
2. Run the program using `python mp3-py.py`.


### Dependencies

External libraries:
  - rich (pip install rich or check out [rich](https://github.com/Textualize/rich))

Standard:
 - os
 - re
 - json
 - argparse
 - shutil
 - rich


## File formatting examples

Default format output 

        -> [{artist}][{title}][{features}][{misc}][{youtube_id}].{filetype}

As of right now the file really just needs to end in ' [youtubeid].filetype' and it should be able to format it to an extent.

        mp3-py.py create --formatfile 'YG Feat. Dj Mustard "Pop It, Shake It" (Uncut) (WSHH Exclusive - Official Music Video) [kQ2KSPz4iSw].wav' -> 
              [YG][Pop It, Shake It][Dj Mustard][Uncut, WSHH Exclusive - Official Music Video][kQ2KSPz4iSw].wav
              
        mp3-py.py create --formatfile 'The Weeknd - Blinding Lights (Lyrics) [4NRXx6U8ABQ].mp3' -> 
              [The Weeknd][Blinding Lights][UNKNOWN][Lyrics][4NRXx6U8ABQ].mp3
              
        mp3-py.py create --formatfile 'Lady Gaga, Ariana Grande - Rain On Me (Official Music Video) [AOm9Fv8NTG0].mp3' -> 
              [Lady Gaga, Ariana Grande][Rain On Me][UNKNOWN][Official Music Video][AOm9Fv8NTG0].mp3

        mp3-py.py create --formatfile 'Music for Sleeping and Deep Relaxation: Delta Waves [HU3ZGMaVZj0].mp4' -> 
              [Music for Sleeping and Deep Relaxation][Delta Waves][UNKNOWN][UNKNOWN][HU3ZGMaVZj0].mp4

        mp3-py.py create --formatfile 'Music [HU3ZGMaVZj0].mp4' -> 
              [Music][UNKNOWN][UNKNOWN][UNKNOWN][HU3ZGMaVZj0].mp4

If these 5 files were formatted with --dirs after filename formatting, it would create directories based off of the unique artist names- 'YG', 'The Weeknd', 'Lady Gaga, Ariana Grande', 'Music for Sleeping and Deep Relaxation' and 'Music' 
in this case - each containing the songs of the artist.

It usually handles trickier filenames okay too (still needs to end in ' [youtubeid].filetype')

        mp3-py.py create --formatfile 'Zacari (adasdasdasd) ft. Isaiah Rashad [misc misc] - Bliss (Official Audio) [audio] [9o1gLWxHI7Q].mp3'i ->
              [Zacari][Bliss][Isaiah Rashad][adasdasdasd, Official Audio, misc misc, audio][9o1gLWxHI7Q].mp3 

        mp3-py.py create --formatfile 'ZillaKami x SosMula ＂33rd Blakk Glass＂(WSHH Exclusive - testing) [9o1gLWxHI7Q].mp3'
              [ZillaKami x SosMula][33rd Blakk Glass][UNKNOWN][WSHH Exclusive - testing][9o1gLWxHI7Q].mp3 


## Demo

First run on anything more than ~5 files. This is why I made the program so I wasnt really too worried about ironing out things too much. If anyone has interest though I can keep working on it. Ill probably do my 'roadmap' tasks and not much more unless other people find it useful. 

https://user-images.githubusercontent.com/71906074/221419033-9617af86-928f-40ec-a9c1-9d011a2f248f.mp4


## Usage

The MP3-PY tool includes two main commands: `create` and `view`.


### Create Sub-Command

The create sub-command has three optional arguments: --dirs, --formatfile, and --formatdir. These are used to process formatted MP3 files from a directory into artist directories and to format MP3 filenames according to a specific pattern.
              
                python mp3-py.py create --dirs DIRECTORY
                python mp3-py.py create --formatfile FILENAME
                python mp3-py.py create --formatdir DIRECTORY


### View Sub-Command

The view sub-command has three sub-commands: json, artists, and songs. The json sub-command has one optional argument: --dump, which is used to create a JSON of formatted MP3 files in a specified directory. The artists sub-command has two optional arguments: --tracks to list all artists in the dataset and their tracks, and --names to list all artists in the dataset. The songs sub-command has three optional arguments: --artist to specify the artist to display songs for, --id to search for a song by YouTube ID, and --name to search for a song by track title.
              
                python mp3-py.py view --data DATASET json --dump DIRECTORY (DATASET will be overwritten or created)

                python mp3-py.py view --data DATASET artists --tracks
                python mp3-py.py view --data DATASET artists --names
                python mp3-py.py view --data DATASET songs --artist ARTIST
                python mp3-py.py view --data DATASET songs --id YOUTUBE_ID
                python mp3-py.py view --data DATASET songs --name TRACK_TITLE

              
### MP3Create class

The MP3Create class has three methods: dirs(), format_file(), and format_files_dir(). The dirs() method is used to process formatted MP3 files from a directory into artist directories. The format_file() method is used to format an MP3 filename according to a specific pattern. The format_files_dir() method is used to format MP3 filenames in a specified directory according to a specific pattern.


### MP3View class

The MP3View class has six methods: json_dump(), get_artists(), get_artists_tracks(), get_songs_by_artist(), get_songs_by_id(), and get_songs_by_name(). The json_dump() method is used to create a JSON of the dataset. The other methods are used to query the dataset and return the results in Markdown format.


### Example dataset

      {
        "Koly P": {
          "tracks": [
            {
              "title": "Rapture Of Thugs",
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
              "video_id": "NpcsssBx2Y0",
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

 - Allow to confirm/deny filename changes
 - General regex adjusting for broader use
 - Refactoring code for better readability and maintainability
 - Bug fixes and optimization


## License

This project is licensed under the MIT License. See the LICENSE file for more information.
