import os

from rich import markdown
from rich import print
from classes.command_processor import CommandProcessor
from classes.database_controller import DatabaseController

header_text = """
# LINUX BOOK
#### By - Ashwin Sharma

- A centralized collection of various "linux commands" so that you don't ever get stuck again struggling to recall 
the right command. - Type ` /h ` for help
"""

def entry_point():

    # Initialize database
    dbc = DatabaseController()
    dbc.ensure_existing()

    # Clear any pre-existing clutter
    os.system('cls' if os.name == 'nt' else 'clear')
    print(markdown.Markdown(header_text, hyperlinks=True))

    # Interactive prompts here
    while True:

        print("\n\n\n[bold #aa88ff] >> [/bold #aa88ff] ", end="")
        choice = input("")

        if choice != "/clear":
            processor = CommandProcessor()
            processor.set_expression(choice)
            processor.interpret_command()

        elif choice == "/clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(markdown.Markdown(header_text, hyperlinks=True))

        else:
            print("Some internal error occured")


# Initiating entry pointsettings
if __name__ == "__main__":
    entry_point()
