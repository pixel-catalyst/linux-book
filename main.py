import os
import sqlite3

from rich import markdown
from rich import print
from classes.command_processor import CommandProcessor

header_text = """
# LINUX BOOK
#### By - Ashwin Sharma

- A centralized collection of various "linux commands" so that you don't ever get stuck again struggling to recall 
the right command. - Type ` /h ` for help"""

# Create a new SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()
# Create a table to store key-value pairs
c.execute('''CREATE TABLE IF NOT EXISTS keyvalue
             (key TEXT PRIMARY KEY, value TEXT)''')


# Interactive interface
def entry_point():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(markdown.Markdown(header_text, hyperlinks=True))
    """Entry point for the interactive interface"""
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

# Close the database connection
conn.close()
