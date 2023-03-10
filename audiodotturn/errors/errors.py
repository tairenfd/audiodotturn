'''
errors.py
---------

Constructors available
----------------------
    __init__(self, exception: Exception, setopts: Tuple[str, ...], console: Console, error_opt: Optional[str] = None, debug: bool = False, if_exit: bool = False)
        Initializes the AudiodotturnError instance.
        
        Parameters:
            exception (Exception): The exception that was raised.
            setopts (Tuple[str, ...]): The error message options set in the config.
            error_opt (Optional[str]): Set a specific option and run only that option. Mainly for backend use. Default value is None.
            debug (bool): Whether to include traceback in error message. Mainly for backend use. Default value is False.
            console (Console): A Rich console instance to output error messages.
            if_exit (bool): Whether to call sys.exit() if the error is critical. Default value is False.

        Returns:
            None

Methods available
-----------------
    __str__(self) -> str
        Returns the currently set error message options as a string.
        
        Returns:
            str: Currently set error message options.

    get_error_options(self) -> str
        Returns available error message options with their descriptions.
        
        Returns:
            str: Error message options with their descriptions.

    handle_error(self)
        Handles the error messages according to the set options. Calls sys.exit() only if exit=True or error is critical.

        Returns:
            None

Notes
-----
None.
'''
import sys
import traceback
from typing import Tuple, Optional
from rich.console import Console


class AudiodotturnError():
    """
    Class for errors in audiodotturn.
    """

    def __init__(self, exception: Exception, setopts: Tuple[str, ...], console: Console, error_opt: Optional[str] = None, debug: bool = False, if_exit: bool = False):
        """
        Constructor for AudiodotturnError class.

        Args:
            exception (Exception): Exception that was raised
            setopt (Tuple[str, ...]): Error message options set in config.
            error_opt (Optional[str]): Set a specific option, only run that option. Mainly for backend use.
            traceback_msg (bool): Whether to include traceback in error message. Mainly for backend use.

        Returns:
            None
        """
        self.exception = exception
        self.setopts = setopts
        self.error_opt = error_opt
        self.debug = debug
        self.console = console
        self.exit = if_exit
        self.error_options = {
            "error": "Critical error that will stop program execution.",
            "warning": "Non-critical issue that may affect program functionality.",
            "info": "Informational message for user.",
            "traceback": "Detailed error information for debugging.",
            "custom": "Custom error message defined by the user."
        }

        self.handle_error()

    def __str__(self) -> str:
        """
        Get currently set error message options.

        Returns:
            str: Currently set error message options.
        """
        return ', '.join(self.setopts)

    def get_error_options(self) -> str:
        """
        Get available error message options

        Returns:
            str: Error message options
        """
        options = []
        for item in self.error_options.items():
            options.append(f'option: {item[0]}, description: {item[1]}')
        return '\n'.join(options)

    def handle_error(self):
        """
        Handle error message.

        Returns:
            None: Calls sys.exit() only if exit=True or error is critical.
        """
        opts = list(self.setopts)

        def traceback_msg(self):
            if self.debug:
                self.console.log(f"[magenta]Exception -> {self.exception.__repr__}")
            tb = self.exception.__traceback__
            tb_txt = "".join(traceback.format_list(traceback.extract_tb(tb)))
            self.console.log(f"[magenta]Traceback -> {tb_txt}")

        if self.error_opt:
            opts = [self.error_opt]
        if self.debug:
            traceback_msg(self)


        for msg in opts:
            if msg == "error":
                self.console.log(f"[yellow]Error -> [red]{sys.exception()}")
            elif msg == "warning":
                self.console.log(f"[yellow]Warning -> [red]{sys.exception()}")
            elif msg == "info":
                self.console.log(f"[yellow]Info -> [blue]{sys.exception()}")
            elif msg == "traceback":
                traceback_msg(self)
            elif msg not in self.error_options:
                self.console.log(f"[yellow]Custom -> {msg}")

        if self.exit:
            sys.exit(1)
