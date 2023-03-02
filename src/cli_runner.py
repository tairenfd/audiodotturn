import argparse
import sys
from src.parsers import parsers, args, defaults
from src.commands import Create, View
from src import VERSION
import json
from rich.json import JSON
from rich.markdown import Markdown
from rich.prompt import Confirm

# CLI runner
class CLI:
    def __init__(self, args: argparse.Namespace, parsers: tuple((argparse.ArgumentParser, ...))):
        # initiate args and parsers
        self.args = args
        self.parser = parsers[0]
        self.create_parser = parsers[1]
        self.view_parser = parsers[2]

        if self.args.version:
            defaults.console.print(Markdown(f'# {VERSION}'))
            sys.exit(1)
            

        # display defaults (--defaults)
        if self.args.defaults:
            display = self.args.defaults
            if display == 'options':
                defaults.display_options()
            elif display == 'format':
                defaults.display_formatting_defaults()
            elif display == 'program':
                defaults.display_program_defaults()
            elif display == 'all':
                defaults.display_all()
            sys.exit(1)

        elif self.args.command == 'set':

            updated = False
            changes = {
                "changed": [],
                "unchanged": []
            }
            for arg_name, arg_value in vars(args).items():
                if arg_name not in ['dry', 'command', 'version', 'default'] and arg_value is not None:
                    updated = False
                    _store_set = None
                    if arg_name == "dry_set":
                        _store_set = arg_name
                        arg_name = "dry"
                    defaults.console.log(f"\n\n[bold magenta]Changes being made to: [bold cyan]{arg_name} -> [bold green]{str(arg_value)} from [orange]{getattr(defaults, arg_name)}\n")
                    confirmed = Confirm.ask(prompt="\n[bold white]Are you sure you want to make these changes?", console=defaults.console)
                    if not confirmed:
                        changes["unchanged"].append(arg_name)
                        defaults.console.log("\n\n[yellow]Setting will not be changed\n\n.")
                    updated = True if confirmed else updated
                    if updated:
                        if _store_set:
                            arg_name = _store_set
                        changes["changed"].append(arg_name)
                        run = getattr(defaults, f'set_{arg_name}')
                        run(arg_value)

            defaults.console.log("Short summary of changes: \n", JSON(json.dumps(changes)))
            if changes["changed"]:
                updated = True

            with defaults.console.status("[bold green]Working...") as status:
                if updated:
                    defaults.write_config(dry=self.args.dry)
                    if self.args.dry:
                        defaults.console.log("\n[green]Defaults would have been updated successfully!")
                    else:
                        defaults.console.log("\n[green]Defaults updated successfully!")
                defaults.console.log("\n[red]No settings were updated. If you did not run in dry mode then something went wrong.")
                sys.exit(1)

        # create - positional arg
        elif self.args.command == 'create':
            # initialize creator
            creator = Create(self.args)

            # If no args send help text
            if not any((self.args.dirs, self.args.formatfile, self.args.formatdir, self.args.dump)):
                self.create_parser.print_help()
                sys.exit(1)
            
            # run creator
            creator.run()

        # view - positional arg
        elif args.command == 'view':
            # initialize viewer
            viewer = View(self.args)

            # If no data arg send help text
            if not self.args.data:
                self.view_parser.print_help()
                sys.exit(1)
            
            # run viewer
            if any(args.view_command):
                viewer.run()


        # if no positional args or request for defaults, send help text
        else:
            self.parser.print_help()

def main() -> None:
    # Run cli
    CLI(args=args, parsers=parsers)

if __name__ == "__main__":
    main()
