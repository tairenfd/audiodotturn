import argparse
from rich.markdown import Markdown
from audiodotturn.config import defaults
from audiodotturn import VERSION
from audiodotturn.parsers import Parser
from audiodotturn.commands import Create, View, Set

# Get default settings

class CLI:
    """
    A command-line interface runner that handles the parsing of
    arguments and their subsequent execution.
    """
    def __init__(self, args: argparse.Namespace, parsers: tuple((argparse.ArgumentParser, ...))):
        """
        Initializes the CLI with the given arguments and parsers.

        Args:
            args (argparse.Namespace): The arguments passed to the CLI.
            parsers (tuple((argparse.ArgumentParser, ...))): The parsers for the CLI.
        
        Returns:
            None
        """
        self.args = args
        self.parser = parsers[0]
        self.create_parser = parsers[1]
        self.view_parser = parsers[2]

    def run(self) -> None:
        """
        Executes the appropriate action based on the CLI arguments.

        Returns:
            None
        """
        if self.args.version:
            self.show_version()

        elif self.args.defaults:
            self.show_defaults()

        elif self.args.command == 'set':
            setter = Set(self.args)
            setter.run()

        elif self.args.command == 'create':
            creator = Create(self.args)
            # If no args send help text
            if not any((self.args.dirs, self.args.formatfile, self.args.formatdir, self.args.dump)):
                self.create_parser.print_help()
                return
            # run creator
            creator.run()

        elif self.args.command == 'view':
            # initialize viewer
            viewer = View(self.args)
            # If no data arg send help text
            if not self.args.data:
                self.view_parser.print_help()
                return
            # run viewer
            if any(self.args.view_command):
                viewer.run()

        else:
            self.parser.print_help()

    def show_version(self) -> None:
        """
        Shows the current version of the program.

        Returns:
            None
        """
        defaults.console.print(Markdown(f'# {VERSION}'))

    def show_defaults(self):
        """
        Shows the default values for the program options.
    
        Returns:
            None
        """
        display = self.args.defaults
        if display == 'options':
            defaults.display_options()
        elif display == 'format':
            defaults.display_formatting_defaults()
        elif display == 'program':
            defaults.display_program_defaults()
        else:
            defaults.display_all()

def main() -> None:
    """
    Get args from main parser    
    Initialize and start the CLI runner

    Returns:
        None
    """
    # Run cli
    parser = Parser()
    parsers = parser.get_parsers()
    args = parser.parse_args()
    cli = CLI(args=args, parsers=parsers)
    cli.run()

if __name__ == "__main__":
    main()
