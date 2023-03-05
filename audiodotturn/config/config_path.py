"""
Module used to initialize CONFIG_PATH for audiodotturn config.

ADT_CONFIG_PATH is a list of common configuration paths for a Linux environment.

.. todo::
   Add option for shell env to be set for CONFIG_PATH.

.. note::
   Failure of this module will result in sys.exit.

"""
import os
import sys
from rich.console import Console
import pkg_resources

console = Console()
# Check common configuration paths
ADT_CONFIG_PATH = [
    os.path.expanduser("~/.config/audiodotturn/adt_config.json"),
    os.path.expanduser("~/config/audiodotturn/adt_config.json"),
    os.path.expanduser("~/audiodotturn/adt_config.json"),
    os.path.expanduser("~/adt_config.json"),
    "/usr/local/etc/audiodotturn/adt_config.json",
    "/etc/audiodotturn/adt_config.json",
]

CONFIG_PATH = None

for path in ADT_CONFIG_PATH:
    if os.path.exists(path):
        CONFIG_PATH = path
        break

if not CONFIG_PATH:
    console.log('[bold yellow]User config not found, falling back to default config.')
    CONFIG_PATH = pkg_resources.resource_filename(__name__, "config.json")
    if not CONFIG_PATH:
        console.log('[bold red]Error loading default config.')
        sys.exit(1)
