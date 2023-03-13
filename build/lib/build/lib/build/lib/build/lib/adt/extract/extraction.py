import re
import json
import os
from typing import Union, List, LiteralString, Any, Dict
import yaml

class Extractor:
    """
    A class for extracting metadata from file names.

    Methods:
        __init__(exts: LiteralString = None)
            Initializes an instance of the Extractor class with an optional list of file extensions.
        
        get_extraction(opt: str = "dict") -> Union[str, List, Dict]
            Returns the extracted data in a specified format.
        
        false_extract(_file: LiteralString) -> Dict[str, Union[str, Any]]
            Sets the most current extraction as unsuccessful and sets the `extracted_data` attribute with the extracted data.
        
        true_extract(info: List[Any]) -> Dict[str, Union[str, Any]]
            Sets the most current extraction as successful and sets the `extracted_data` attribute with the extracted data.
        
        simple_extract(_file: LiteralString) -> List[Any]
            Performs a simple extraction of metadata from a file name. The extracted data is set to the `extracted_data` attribute.
        
        complex_extract(filename: LiteralString) -> None
            Performs a complex extraction of metadata from a file name. The extracted data is set to the `extracted_data` attribute.

    Attributes:
        exts: Tuple of strings
            The file extensions that the extractor class will attempt to extract metadata from.
        
        output_opts: List of strings
            The available output format options for the extracted data.
        
        extracted_data: Dict[str, Union[str, Any]]
            The extracted metadata from the last extraction.
    """
    # initialize extractor instance with optional extension list
    def __init__(self, exts: List, output_opts = List):
        """
        Initializes an instance of the Extractor class with an optional list of file extensions.

        Parameters:
            exts: list of exts to format
            output_opts: available output opts, this should be the opts in the program defaults.
        """

        self.exts = tuple(exts)
        self.output_opts = output_opts
        self.extracted_data = None

    def get_extraction(self, opt: str = "dict"):
        """
        Returns the currently extracted data in a specified format.

        Parameters:
            opt: str, optional
                The desired format for the extracted data. The default format is "dict". The available format options are:
                "dict", "json", "yaml", "str", "list", "keys", and "values".

        Returns:
            The extracted data in the specified format. The format will depend on the specified `opt` parameter.

        Raises:
            None
        """
        if opt and opt.lower() in self.output_opts and self.extracted_data:
            match opt:
                case "json":
                    return json.dumps(self.extracted_data)
                case "yaml":
                    return yaml.dump(self.extracted_data)
                case "dict":
                    return self.extracted_data
                case "str":
                    return str(self.extracted_data)
                case "list":
                    return list(self.extracted_data.values())
                case "keys":
                    return list(self.extracted_data.keys())
                case "values":
                    return list(self.extracted_data.values())
                case _:
                    return self.extracted_data
        else:
            raise UserWarning("Extracted data is empty")

    # unsuccessful extraction
    # sets current instances most current extraction via
    # extracted-data property
    def false_extract(self, _file: LiteralString) -> Dict[str, Union[str, Any]]:
        """
        Sets the current extraction as an unsuccessful extraction, unsucceful extractions
        simply contain the original file name and a False status, all metadata values are set
        to None

        Parameters:
            _file: str
                The file name to extract metadata from.

        Returns:
            A dictionary containing the unsuccessful extraction data.

        Raises:
            TypeError:
                If `_file` is not a string.
        """
        if not isinstance(_file, str):
            raise TypeError("file must be a str literal")

        self.extracted_data = {
            "original_file": _file,
            'artist': None,
            'title': None,
            'features': None,
            'misc': None,
            'youtube_id': None,
            'filetype': None,
            "status": False
        }

    # successful extraction
    # sets current instances most current extraction via
    # extracted-data property
    def true_extract(self, info: List[Any]) -> Dict[str, Union[str, Any]]:
        """
        Sets the most current extraction as successful and sets the `extracted_data` attribute with the extracted data.

        Parameters:
            info: List
                A list containing the extracted metadata.

        Returns:
            A dictionary containing the successful extraction data.

        Raises:
            TypeError:
                If `info` is not a list.
        """
        if not isinstance(info, List):
            raise TypeError("info must be a list of 7 values")

        self.extracted_data = {
            "original_file": info[0],
            'artist': info[1],
            'title': info[2],
            'features': info[3],
            'misc': info[4],
            'youtube_id': info[5],
            'filetype': info[6],
            "status": info[7]            
        }


    # simple extraction for if you already know the formatting to an extent
    def simple_extract(self, _file: LiteralString) -> List[Any]:
        """
        Extracts information from a filename in a specific format and returns the extracted
        data as a list containing eight values: the original filename, the artist info, title
        info, features info, misc info, youtube_id info, the file extension, and the extractions
        status value (True or False depending on whether data was sent to the `true_extract` method
        or the `false_extract` method by the Extractor).

        If the filename info is extracted successfully, the method uses the `true_extract` method
        to set the current extract data. If unsuccessful, the method uses the `false_extract` method
        to set the current extract data. Current extract data always contains the last extract
        within the current `Extractor()` instance. Extracts are tuples containing eight values:
        the original filename, the artist info, title info, features info, misc info, youtube_id
        info, the file extension, and the extractions status value which will be True or False
        depending on whether data was sent to the `true_extract` method or the `false_extract`
        method.

        Parameters:
            _file (LiteralString): The filename to extract information from.

        Returns:
            List[Any]: The extracted information in the form of a list containing eight values:
                the original filename, the artist info, title info, features info, misc info,
                youtube_id info, the file extension, and the extractions status value.
        """

        if not isinstance(_file, str):
            raise TypeError("file must be a str literal")

        _file = os.path.basename(_file)

        if not _file.endswith(self.exts):
            return self.false_extract(_file)

        format_check = re.search(
            r"\[(.+?)\][ ]?\[(.+?)\][ ]?\[(.+?)\][ ]?\[(.+?)\][ ]?\[(.+?)\][ ]?\.(\w+)$", _file
        ) or re.search(
            r"^(.+?)[ ]?-[ ](.+?) ft\. (.+?) \((.+?)\) \[(.+?)\]\.(\w+)$|^(.+?)[ ]-[ ]?(.+?)ft\.(.+?)\((.+?)\) \[(.+?)\]\.(\w+)$",
            _file
        ) or re.search(
            r"\((.+?)\)[ ]?\((.+?)\)[ ]?\((.+?)\)[ ]?\((.+?)\)[ ]?\((.+?)\)[ ]?\.(\w+)$", _file
        )

        if format_check:

            return self.true_extract([
                    _file,
                    format_check[1],
                    format_check[2],
                    format_check[3],
                    format_check[4],
                    format_check[5],
                    format_check[6],
                    True
                ])

        format_check = re.search(
            r"\[(.+?)\][ ]?\[(.+?)\][ ]?\[(.+?)\][ ]?\[(.+?)\]\.(\w+)$",
            _file
        ) or re.search(
            r"^(.+?)[ ]?-[ ](.+?)ft\.(.+?)\((.+?)\)\.(\w+)$|^(.+?)[ ]-[ ]?(.+?)ft\.(.+?)\((.+?)\)\.(\w+)$",
            _file
        ) or re.search(
            r"\((.+?)\)[ ]?\((.+?)\)[ ]?\((.+?)\)[ ]?\((.+?)\)\.(\w+)$",
            _file
        )

        if format_check:

            return self.true_extract([
                    _file,
                    format_check[1],
                    format_check[2],
                    format_check[3],
                    format_check[4],
                    None,
                    format_check[5],
                    True
            ])

        format_check = re.search(
            r"\[(.+?)\][ ]?\[(.+?)\][ ]?\[(.+?)\]\.(\w+)$", _file
        ) or re.search(
            r"\((.+?)\)[ ]?\((.+?)\)[ ]?\((.+?)\)\.(\w+)$", _file
        )

        if format_check:
            return self.true_extract([
                    _file,
                    format_check[1],
                    format_check[2],
                    format_check[3],
                    None,
                    None,
                    format_check[4],
                    True
            ])
       
        if not format_check:
            return self.false_extract(_file)

    # 'complex' extraction for any filename
    # if filename info is extracted successfully, then use true extract method to set current
    # extract data
    # if unsuccessful, use the false extract method to set current extract data
    # current extract data will always contain the last extract within the current
    # Extractor() instance
    # extracts are tuples containing 8 values, the original filename, the artist info, title
    # info, features info, misc info, youtube_id info, the file extension, and the extractions
    # status value which will be True or False depending on if data was sent to true extract method
    # or false extract method
    def complex_extract(self, _file: LiteralString) -> List[Any]:
        """
        Extracts information from a filename and returns the extracted data as a list containing
        eight values: the original filename, the artist info, title info, features info, misc info,
        youtube_id info, the file extension, and the extractions status value (True or False
        depending on whether data was sent to the `true_extract` method or the `false_extract`
        method by the Extractor).

        If the filename info is extracted successfully, the method uses the `true_extract` method
        to set the current extract data. If unsuccessful, the method uses the `false_extract` method
        to set the current extract data. Current extract data always contains the last extract
        within the current `Extractor()` instance. Extracts are tuples containing eight values:
        the original filename, the artist info, title info, features info, misc info, youtube_id
        info, the file extension, and the extractions status value which will be True or False
        depending on whether data was sent to the `true_extract` method or the `false_extract`
        method.

        Parameters:
            _file (LiteralString): The filename to extract information from.

        Returns:
            List[Any]: The extracted information in the form of a list containing eight values:
                the original filename, the artist info, title info, features info, misc info,
                youtube_id info, the file extension, and the extractions status value.
        """

        if not isinstance(_file, str):
            raise TypeError("file must be a str literal")

        _file = os.path.basename(_file)

        if not _file.endswith(self.exts):
            return self.false_extract(_file)

        self.simple_extract(_file)
        check = self.get_extraction("dict")
        if check["status"]:
            return

        # create a copy of the filename, one for editing, one for backup
        __file = _file

        # check for track features
        feature_regex_list = [
            (r"\([fF]t[\. | ](.+?)\)", 1),
            (r"([fF]t[\. | ]|[wW]\/)(.+?)(?=([\'\"\.]|[()]|[-]|[\[]))", 2),
            (r"\([fF]eat[\. | ](.+?)\)", 3),
            (r"([fF]eat[\. | ](.+?)(?=([\'\"\.]|[()]|[-]|[\[])))", 4),
        ]

        features = []

        for regex in feature_regex_list:

            features_match = re.search(regex[0], _file)
            group = 1 if regex[1]%2 else 2

            if features_match:
                _file = _file.replace(features_match[0].strip("-[("), "")
                features.append(features_match.group(group).strip("-[(").strip())

        # check for possible youtube id
        youtube_id_regex = re.search('[A-Za-z0-9_-]{11}', _file)
        youtube_id = None
        if youtube_id_regex:
            youtube_id = youtube_id_regex[0]
            _file = _file.replace(youtube_id, '').replace('()', '').replace('[]', '')

        # check for misc info
        misc_regex = re.findall(r"(\(.+?\))|(\[.+?\])|([pP]rod [bB ]y \w*)", _file)
        misc_list = []

        if misc_regex:
            for match in misc_regex:
                _match = match[0] if match[0] else None
                _match = match[1] if _match is None else _match
                _match = match[2] if _match is None else _match
                if _match:
                    _file = _file.replace(_match, "").replace("  ", " ").strip("()[] ")
                    misc_list.append(_match.strip("()[] "))

        # check for rest of values, first for a artist-title combo and then just for artist
        common_regex = re.search(
            r"^(.+?)[ ]?-[ ](.+?)\.(\w+)$|^(.+?)[ ]-[ ]?(.+?)\.(\w+)$|^(.+)\.(\w+)$",
            _file
        )

        # at this point if file cant be formatted, return with a false extract
        if not common_regex:
            return self.false_extract(__file)

        # if file is formattable, check for existing data and fill it in. Use defaults set in config
        # for cases where no info is available.
        features = ', '.join(features) if features else None
        misc = ", ".join(misc_list).strip("()") if misc_list else None

        common_groups = [
            (1, 3),
            (4, 6),
            (7, 8)
        ]

        for group in common_groups:

            if common_regex.group(group[0]):

                artist = (
                    common_regex.group(group[0]).strip()
                    if common_regex.group(group[0])
                    else None
                )

                filetype = (
                    common_regex.group(group[1]).strip().rstrip(".")
                    if common_regex.group(group[1])
                    else None
                )

        # if there is no title, double check the artist name to see if its possibly located there
        title = (
            common_regex.group(2).strip()
            if common_regex.group(2)
            else None
        )

        title = (
            common_regex.group(5).strip()
            if common_regex.group(5) and title is None
            else title
        )

        title_in_artist = re.search(r"([\uFF02\"\'\“\”].+?[\uFF02\"\'\“\”])|([：:•].+)", artist)

        if title_in_artist and title is None:

            if title_in_artist.group(1):
                artist = artist.replace(title_in_artist.group(1), "").strip()
                title = title_in_artist.group(1)

            else:
                artist = artist.replace(title_in_artist.group(2), "").strip()
                title = title_in_artist.group(2)

        if artist is None:
            artist = re.search(r"(.+?)\.(\w+)$", _file)
            artist = artist.group(1)

        # redundant file stripping
        if title is not None:
            title = title.strip("-：:•\uFF02\"'“ ")
        artist = artist.strip("-：:•\uFF02\"'“() ")

        # create formatted file name
        return self.true_extract([
                __file,
                artist,
                title,
                features,
                misc,
                youtube_id,
                filetype,
                True
        ])

    # extracts data from a list of files, allows selection of an output opt
    # which is set to "dict" by default. returns a list of extractions.
    # all extractions are tuples containing 8 values.
    def extract_complex_list(self, file_list: List[str], opt: str = "dict"):
        """
        Extracts data from a list of files using the `complex_extract` method from the `extract` module. 
        Allows selection of an output option, which is set to "dict" by default. Returns a list of 
        extractions, where each extraction is a tuple containing 8 values.

        get_extraction method not necessary to call after use of this method, a list of extractions is
        returned. get_extraction in this case would return the last extraction preformed.

        Parameters:
            file_list (List[str]): A list of file paths from which data is to be extracted.
            opt (str, optional): 
                An output option that determines the format of the extracted data. Defaults to "dict". 
                The supported options are "dict", "list", and "tuple".

        Returns:
            List: A list of extractions, where each extraction is a tuple containing 8 values.

        Raises:
            TypeError: 
                If the `file_list` parameter is not a list of strings or if the `opt` parameter
                is not a string corresponding to the supported options.
        """
        _extractions = []
        if isinstance(file_list, list) and isinstance(opt, str):
            for _file in file_list:
                self.complex_extract(_file)
                _extractions.append(self.get_extraction(opt.strip().lower()))
            return _extractions

        raise TypeError(
            "File_list must be a list of strings. Opt should be a string corresponding to output options"
        )
