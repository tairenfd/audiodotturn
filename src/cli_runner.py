import argparse
from src.parsers import parsers, args, defaults
from src.commands import Create, View

# CLI runner
class CLI:
    def __init__(self, args: argparse.Namespace, parsers: tuple((argparse.ArgumentParser, ...))):
        # initiate args and parsers
        self.args = args
        self.parser = parsers[0]
        self.create_parser = parsers[1]
        self.view_parser = parsers[2]

        # display defaults (--defaults)
        if self.args.defaults:
            defaults.display()
            exit(1)

        # create - positional arg
        elif self.args.command == 'create':
            # initialize creator
            creator = Create(self.args)

            # If no args send help text
            if not any((self.args.dirs, self.args.formatfile, self.args.formatdir)):
                self.create_parser.print_help()
                exit(1)
            
            # run creator
            creator.run()

        # view - positional arg
        elif args.command == 'view':
            # initialize viewer
            viewer = View(self.args)

            # If no data arg send help text
            if not self.args.data:
                self.view_parser.print_help()
                exit(1)
            
            # run viewer
            if any(args.view_command):
                viewer.run()


        # if no positional args or request for defaults, send help text
        else:
            self.parser.print_help()

def main():
    # Initiate tool
    tool = CLI(args=args, parsers=parsers)

if __name__ == "__main__":
    main()