import sys
import traceback
from rich.console import Console

def error_handler(error_msg: list, console: Console, error: Exception) -> None:
    """
    General error message handling for audiodotturn

    Args:
        list: error_msg list produced by config, typically self.error_msg
        rich.console.Console: rich console to use
        Exception: Exception being handled

    Returns:
        None: Calls sys.exit()
    """
    if "error" in error_msg:
        console.log(f'[yellow]Error -> [red]{error}')
        error_msg.remove("error")
    if "traceback" in error_msg:
        error_msg.remove("traceback")
        tb = sys.exception().__traceback__
        tb_txt = ''.join(traceback.format_list(traceback.extract_tb(tb)))
        console.log(tb_txt)
    if error_msg:
        console.log('\n'.join(error_msg))
    sys.exit(1)