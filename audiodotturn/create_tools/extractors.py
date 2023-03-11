'''
extractors.py
-------------

The `extractors` module provides various extractor classes for extracting information from filenames.

Extractors return a dict of values from a file that correspond to most or all of the default formatting options
depending on the choice of extractor.

The dicts can later be constructed into constructed filenames with a file constructor.

Classes
-------
- `BaseExtractors`
- `StandardExtractor`
- `YoutubeExtractor`
'''
import re
from audiodotturn.config import Config
from audiodotturn.errors import AudiodotturnError

EXTRACTORS = {
    'standard': ['standard', 'default', 'normal'],
    'youtube': ['youtube', 'yt']
}

class BaseExtractor:
    '''
    Base class for extractors.

    Attributes:
        config (Config): Configuration object.
        file (str): The name of the file to be formatted.
        format_defaults (dict): Default formatting options.
        dry (bool): Whether the program is in dry run mode.
        features (List[str]): List of track features.
        extractor (str): The name of the extractor.

    Properties:
        extractor (str): Getter and setter for the extractor.

    Methods:
        base_extract(): Extracts data from the filename.
    '''
    def __init__(self, config: Config, extractor: str = "standard"):
        """
        Initializes the BaseExtractor object.

        Args:
            config (Config): Configuration object.
            extractor (str): The name of the extractor.
        """
        self.config = config
        self.file = None
        self.format_defaults = self.config.defaults.formatting
        self.dry = self.config.defaults.program.dry
        self.features = []
        self.extractor = self.config.defaults.program.extractor or extractor

    @property
    def extractor(self):
        """
        Getter for the extractor.

        Returns:
            str: The extractor name.
        """
        return self._extractor

    @extractor.setter
    def extractor(self, extractor):
        """
        Setter for the extractor.

        Args:
            extractor (str): The name of the extractor.
        """
        for extractor_type, aliases in EXTRACTORS.items():
            if extractor in aliases or extractor == extractor_type:
                self._extractor = extractor_type
                return self._extractor
        self.config.console.log(f"[bold red]Formatter *{extractor}* not found! [green]Falling back to *standard* formatter.")
        self._extractor = "standard"
        return self._extractor

    def base_extract(self) -> tuple:
        """
        Extracts data from the filename.

        Returns:
            tuple: The extracted data.
        """
        _file = self.file
            
        if not self.file.endswith(tuple(self.config.program_defaults.exts)):
            return self.file, False

        
        # block base
        stat = None if self.config.program_defaults.constructor == "block" else True

        format_check_block = re.search(
            r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(\w+)$", self.file
        )
        format_check_block2 = re.search(
            r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(\w+)$", self.file
        )
        format_check_block3 = re.search(
            r"\[(.+?)\]\[(.+?)\]\[(.+?)\]\.(\w+)$", self.file
        )
        if format_check_block:
            return (
                {
                    'artist': format_check_block[1].strip().title(),
                    'title': format_check_block[2].strip(),
                    'features': format_check_block[3].strip().title(),
                    'misc': format_check_block[4].strip(),
                    'youtube_id': format_check_block[5],
                    'filetype': format_check_block[6]
                },
                stat
            )
        if format_check_block2:
            return (
                {
                    'artist': format_check_block2[1].strip().title(),
                    'title': format_check_block2[2].strip(),
                    'features': format_check_block2[3].strip().title(),
                    'misc': format_check_block2[4].strip(),
                    'youtube_id': self.config.format_defaults.youtube_id,
                    'filetype': format_check_block2[5]
                },
                stat
            )
        if format_check_block3:
            return (
                {
                    'artist': format_check_block3[1].strip().title(),
                    'title': format_check_block3[2].strip(),
                    'features': format_check_block3[3].strip().title(),
                    'misc': self.config.format_defaults.misc.strip(),
                    'youtube_id': self.config.format_defaults.youtube_id,
                    'filetype': format_check_block3[4]
                },
                stat
            )
        
        # standard base
        stat = None if self.config.program_defaults.constructor == "standard" else True

        format_check_standard = re.search(r"^(.+?)[ ]?-[ ](.+?)ft\.(.+?)\((.+?)\)\.(\w+)$|^(.+?)[ ]-[ ]?(.+?)ft\.(.+?)\((.+?)\)\.(\w+)$", self.file)
        if format_check_standard:
            return (
                {
                    'artist': format_check_standard[1].strip().title(),
                    'title': format_check_standard[2].strip(),
                    'features': format_check_standard[3].strip().title(),
                    'misc': format_check_standard[4].strip(),
                    'filetype': format_check_standard[5].strip()
                },
                stat
            )

        return False


class StandardExtractor(BaseExtractor):
    '''
    The standard extractor, should work in some capacity with most filenames.

    Methods:
        extract(file: str) -> tuple: Extracts data from the filename.
    '''
    def extract(self, file: str) -> tuple:
        """
        Extracts data from the filename.

        Args:
            file (str): The name of the file to be formatted.

        Returns:
            tuple: The extracted data.
        """
        try:
            if self.extractor != 'standard':
                raise TypeError('Invalid extractor')
        except TypeError as error:
            AudiodotturnError(error, tuple(self.config.program_defaults.error_msg), self.config.console, if_exit=True)

        self.file = file
        check = self.base_extract()
        if check or check is None:
            return check

        # check for track features
        features_1 = re.search(r"\([fF]t[\. | ](.+?)\)", file)
        if features_1:
            file = file.replace(features_1[0], "")

        features_2 = re.search(
            r"([fF]t[\. | ]|[wW]\/)(.+?)(?=([\'\"\.]|[()]|[-]|[\[]))", file
        )
        if features_2:
            file = file.replace(features_2[0].rstrip("-[("), "")

        features_3 = re.search(r"\([fF]eat[\. | ](.+?)\)", file)
        if features_3:
            file = file.replace(features_3[0], "")

        features_4 = re.search(
            r"([fF]eat[\. | ](.+?)(?=([\'\"\.]|[()]|[-]|[\[])))", file
        )
        if features_4:
            file = file.replace(features_4[0].rstrip("-["), "")

        features = [features_1, features_2, features_3, features_4]

        # check for misc info
        match_misc_search = re.findall(r"(\(.+?\))|(\[.+?\])|([pP]rod [bB ]y \w*)", file)
        match_misc = []

        if match_misc_search:
            for match in match_misc_search:
                match = match[0] or match[1] or match[2]
                file = file.replace(match, "").replace("  ", " ")
                match_misc.append(match.strip("()[] "))

        # check for rest of values, first for a artist-title combo and then just for artist
        match = re.search(r"^(.+?)[ ]?-[ ](.+?)\.(\w+)$|^(.+?)[ ]-[ ]?(.+?)\.(\w+)$|^(.+)\.(\w+)$", file)
        # at this point if file cant be formatted, return with (file, False) to signify that file cant be formatted due to too much missing info
        if not match:
            return (self.file, False)

        # if file is formattable, check for existing data and fill it in. Use defaults set in config
        # for cases where no info is available.
        if any(features):
            self.features = []
            if features_1:
                self.features.append(features_1.group(1).strip())

            if features_2:
                self.features.append(features_2.group(2).strip())
            if features_3:
                self.features.append(features_3.group(1).strip())

            if features_4:
                self.features.append(features_4.group(2).strip())

        self.features = ", ".join(self.features).replace("'", "")

        features = self.features if self.features else self.format_defaults.features

        misc = ", ".join(match_misc).strip("()") if match_misc else self.format_defaults.misc

        if match.group(1):
            artist = match.group(1).strip() if match.group(1) else self.format_defaults.artist
            filetype = (
                match.group(3).strip().rstrip(".")
                if match.group(3)
                else self.format_defaults.filetype
            )
        if match.group(4):
            artist = match.group(4).strip() if match.group(4) else self.format_defaults.artist
            filetype = (
                match.group(6).strip().rstrip(".")
                if match.group(6)
                else self.format_defaults.filetype
            )
        if match.group(7):
            artist = match.group(7).strip() if match.group(7) else self.format_defaults.artist
            filetype = (
                match.group(8).strip().rstrip(".")
                if match.group(8)
                else self.format_defaults.filetype
            )

        # if there is no title, double check the artist name to see if its possibly located there
        title = match.group(2).strip() if match.group(2) else self.format_defaults.title
        if title == self.format_defaults.title:
            title = match.group(5).strip() if match.group(5) else title
        title_in_artist = re.search(r"([\uFF02\"\'\“\”].+?[\uFF02\"\'\“\”])|([：:•].+)", artist)
        if title_in_artist and title == self.format_defaults.title:
            if title_in_artist.group(1):
                artist = artist.replace(title_in_artist.group(1), "").strip()
                title = title_in_artist.group(1)
            else:
                artist = artist.replace(title_in_artist.group(2), "").strip()
                title = title_in_artist.group(2)

        if artist.strip() == self.format_defaults.artist:
            artist = re.search(r"(.+?)\.(\w+)$", self.file)
            artist = artist.group(1)
        title = title.strip()
        title = title.rstrip("-：:•\uFF02\"'“")
        title = title.lstrip("-：:•\uFF02\"'“")
        title = title.strip()
        artist = artist.strip()
        artist = artist.rstrip("-：:•\uFF02\"'“")
        artist = artist.lstrip("-：:•\uFF02\"'“")
        artist = artist.strip()

        # create formatted file name
        return ({
                'artist': artist.strip().title(),
                'title': title.strip(),
                'features': features.strip().title(),
                'misc': misc.strip(),
                'filetype': filetype
            }, True)
        

class YoutubeExtractor(BaseExtractor):
    '''
    The youtube extractor, used for when title formats are known to contain a youtube_id at the end formatted as
    [youtube_id].ext, this is common with unformatted yt-dpl files.

    Methods:
        format(file: str) -> dict: Extracts a dict of values from the filename.
    '''
    def format(self, file):
        """
        Extracts a dict of values from the filename.

        Args:
            file (str): The name of the file to be formatted.

        Returns:
            dict: The extracted data.
        """
        # TODO
