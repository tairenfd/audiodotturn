from typing import List, LiteralString, Dict

class Constructor:
    """
    A class for constructing new filenames based on extracted data.

    Attributes:
        data_in : List
            A list of one or more 'extractions' from the Extractor() class.
        success : List
            A list of successful constructions.
        failure : List
            A list of unsuccessful constructions.
        auto : bool
            A flag for whether or not to perform auto-construction.
        constructor : LiteralString
            A string representing the constructor style to use.
    """
    def __init__(self, data_list: List, constructor: LiteralString, auto: bool = False) -> None:
        """
        Load the constructor with the data, a constructor choice and optional auto option.

        Parameters:
            data_list (List): A list of datasets. Each dataset should be a dictionary of extracted data 
                generated by the Extractor() class.
            constructor (LiteralString): A string that sets the constructor style to use. Options are 'custom', 
                'simple', or 'block'.
            auto (bool): An optional boolean that sets whether or not to use auto-construction. Default is False.

        Returns:
            None
        """
        self.data_in = data_list
        self.success = []
        self.failure = []
        self.auto = auto
        self.constructor = constructor

    # return successful constructions
    def get_success(self):
        """
        Returns the list of successful constructions.

        Returns
        -------
            List: A list of successful constructions.
        """
        if self.success:
            return self.success

    # return unsuccessful constructions
    def get_failure(self):
        """
        Returns the list of unsuccessful constructions.

        Returns:
            List: A list of unsuccessful constructions.
        """
        if self.failure:
            return self.failure

    # construction from a list of one or more dicts or json datasets
    # constructions occur for extractions with a status of True indicating
    # that the file info was obtained successfully from Extractor()
    # constructions can be obtained through the get_success method,
    # files that wont be constructed can be obtained through the get_failure method
    def from_dict(self):
        """
        Construction from a list of one or more dicts or json datasets. Constructions occur for extractions with a 
        status of True indicating that the file info was obtained successfully from Extractor(). Constructions can be 
        obtained through the get_success method, files that wont be constructed can be obtained through the 
        get_failure method.

        Parameters:
            None

        Returns:
            None
        """
        # cycle through extractions within the data list
        for _data in self.data_in:

            # if a dataset within the list is not a dict, then raise TypeError
            if not isinstance(_data, Dict):
                raise TypeError("All data in list should be dicts")

            # get the `status` of the current extraction
            status = _data["status"]
            # get the original filename of the current extraction
            original_file = _data["original_file"]

            # if the extraction status = True aka successful, then get the values
            # from the extraction data and send them through the run method - the 
            # resulting tuple will be appended to the `success` property
            if status:
                artist = _data["artist"]
                title = _data["title"]
                features = _data["features"]
                misc = _data["misc"]
                filetype = _data["filetype"]
                youtube_id = _data["youtube_id"]

                self.success.append(
                    self.run(
                        original_file,
                        artist,
                        title,
                        features,
                        misc,
                        filetype,
                        youtube_id
                    )
                )
            if not status:
                self.failure.append(original_file)


    def run(
        self,
        original_file: LiteralString,
        artist: LiteralString,
        title: LiteralString,
        features: LiteralString,
        misc: LiteralString,
        filetype: LiteralString,
        youtube_id: LiteralString
    ) -> tuple:
        """
        Singular construction from extracted values, typically will be called by the other methods within Constructor, 
        returns a tuple containing the original filename and a list containing its new formatting options, if auto is 
        true then the most detailed option is returned with the filename instead of a list of options.

        Parameters:
            original_file (LiteralString): The original filename to be formatted.
            artist (LiteralString): The artist name extracted from the file.
            title (LiteralString): The song title extracted from the file.
            features (LiteralString): Any features of the song, if any.
            misc (LiteralString): Any additional information to be included in the filename, if any.
            filetype (LiteralString): The filetype of the file.
            youtube_id (LiteralString): The youtube id, if available.

        Returns:
            tuple: A tuple containing the original filename and a list of options for the formatted filename. If 
                auto is True, the most detailed option is returned with the filename instead of a list of options.
                Tuple[str, List] or Tuple[str, str]
        """

        if self.constructor == "custom":
            # have user select desired values
            # have user select layout from options generated from selected values
            pass

        if self.constructor == "simple":
            options = [
                f"{artist} - {title}.{filetype}",
                f"{artist} - {title} [{youtube_id}].{filetype}",
                f"{artist} - {title} ({misc}).{filetype}",
                f"{artist} - {title} ft. {features}.{filetype}",
                f"{artist} - {title} ft. {features} ({misc}).{filetype}",
                f"{artist} - {title} ft. {features} [{youtube_id}].{filetype}",
                f"{artist} - {title} ft. {features} ({misc}) [{youtube_id}].{filetype}",
            ]

        elif self.constructor == "enclosed":
            options = [
                f"({artist})({title}).{filetype}",
                f"({artist})({title})({misc}).{filetype}",
                f"({artist})({title})({features}).{filetype}",
                f"({artist})({title})({youtube_id}).{filetype}",
                f"({artist})({title})({features})({misc}).{filetype}",
                f"({artist})({title})({features})({youtube_id}).{filetype}",
                f"({artist})({title})({features})({misc})({youtube_id}).{filetype}"
            ]

        if self.auto:
            return (original_file, options[-1])

        return (original_file, options)
