'''
construction.py
---------------

Module for constructing extracted file information into a formatted string 
that can be used as the new filename.

Constructors available
----------------------
    simple: 
        ex. "artist - title ft. features (misc).ext",
    blocks:
        ex. "[artist][title][features][misc].[ext]"
Notes
-----
None.
'''

class Constructors:
    '''
    Constructor class

    Returns:
        list: list of constructed filename options
    '''
    def __init__(self, extracted_data: dict, constructor: str) -> None:
        """
        Initializes a new instance of the Constructors class.

        Args:
            extracted_data (dict): The extracted data used for filename construction.
            constructor (str): The type of filename constructor to use, either "simple" or "block".
        """
        self.extracted_data = extracted_data
        self.artist = self.extracted_data["artist"]
        self.title = self.extracted_data["title"]
        self.features = self.extracted_data["features"]
        self.misc = self.extracted_data["misc"]
        self.filetype = self.extracted_data["filetype"]
        self.youtube = None
        if len(self.extracted_data) == 6:
            self.youtube_id = self.extracted_data["youtube_id"]
        self.constructor = constructor

    def run(self) -> list:
        """
        Constructs a list of filename options based on the extracted data and the chosen constructor.

        Returns:
            list: A list of constructed filename options.
        """
        if self.constructor == "simple":
            options = [
                f"{self.artist} - {self.title}.{self.filetype}",
                f"{self.artist} - {self.title} ft. {self.features}.{self.filetype}",
                f"{self.artist} - {self.title} ft. {self.features} ({self.misc}).{self.filetype}",
            ]
            if self.youtube is not None:
                options.append(f"{self.artist} - {self.title} ft. {self.features} ({self.misc}).{self.filetype}")

            return options
            
        if self.constructor == "block":
            options = [
                f"[{self.artist}][{self.title}].{self.filetype}",
                f"[{self.artist}][{self.title}][{self.features}].{self.filetype}",
                f"[{self.artist}][{self.title}][{self.features}][{self.misc}].{self.filetype}",
            ]
            if self.youtube is not None:
                options.append(f"[{self.artist}][{self.title}][{self.features}][{self.misc}][{self.youtube_id}].{self.filetype}")

            return options
                