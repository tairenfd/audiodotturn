import argparse
from parsers import parsers, args, defaults
from commands import Create, View


class AudioDotTurn:
    def __init__(self, args: argparse.Namespace, parsers: tuple((argparse.ArgumentParser, ...))):
        self.args = args
        self.parser = parsers[0]
        self.create_parser = parsers[1]
        self.view_parser = parsers[2]

        if self.args.defaults:
            defaults.display()
            exit(1)

        elif self.args.command == 'create':
            creator = Create(self.args)
            if not any((self.args.dirs, self.args.formatfile, self.args.formatdir)):
                self.create_parser.print_help()
                exit(1)
            creator.run()

        elif args.command == 'view':
            viewer = View(self.args)
            if not self.args.data:
                self.view_parser.print_help()
                exit(1)
            if any(args.view_command):
                viewer.run()


        else:
            self.parser.print_help()

def main():
    # Initiate tool
    tool = AudioDotTurn(args=args, parsers=parsers)

if __name__ == "__main__":
    main()
