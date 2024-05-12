import os
import sqlite3

from rich import markdown
from rich import print

header_text = """
# LINUX BOOK
#### By - Ashwin Sharma

- A centralized collection of various "linux commands" so that you don't ever get stuck again struggling to recall the right command.
- Type ` /h ` for help
"""


# Create a new SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()
# Create a table to store key-value pairs
c.execute('''CREATE TABLE IF NOT EXISTS keyvalue
             (key TEXT PRIMARY KEY, value TEXT)''')


def insert_key_value(key, value):
    """Insert a new key-value pair into the database
    :param key:
    :param value:
    """
    try:
        c.execute("INSERT INTO keyvalue VALUES (?, ?)", (key, value))
        conn.commit()
        print(f"Insertion successful!")
    except sqlite3.IntegrityError:
        print(f"Error: Key '{key}' already exists")


def get_value(key):
    """Retrieve the value associated with a given key"""
    c.execute("SELECT value FROM keyvalue WHERE key=?", (key,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        print(f"Error: Key '{key}' not found")
        return None


def update_value(key, new_value):
    """Update the value associated with a given key"""
    c.execute("UPDATE keyvalue SET value=? WHERE key=?", (new_value, key))
    if c.rowcount > 0:
        conn.commit()
        print(f"Value updated for key '{key}'")
    else:
        print(f"Error: Key '{key}' not found")


def delete_key(key):
    """Delete a key-value pair from the database"""
    c.execute("DELETE FROM keyvalue WHERE key=?", (key,))
    if c.rowcount > 0:
        conn.commit()
        print(f"Key '{key}' deleted successfully")
    else:
        print(f"Error: Key '{key}' not found")


def display_all():
    """Display all key-value pairs in the database"""
    c.execute("SELECT * FROM keyvalue")
    result = c.fetchall()
    if result:
        for row in result:
            print(f"Key: {row[0]}, Value: {row[1]}")
    else:
        print("Database is empty")


# Interactive interface
def entry_point():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(markdown.Markdown(header_text, hyperlinks=True))
    """Entry point for the interactive interface"""
    while True:
        # print("\n[bold blue heading]Choose an option:[/bold blue heading]")
        # print("1. Insert a new key-value pair")
        # print("2. Get the value of a key")
        # print("3. Update the value of a key")
        # print("4. Delete a key-value pair")
        # print("5. Display all key-value pairs")
        # print("6. Exit")
        print("\n\n\n[bold blue] >> [/bold blue] ", end="")
        choice = input("")

        if choice == "/new":
            key = input("Enter the key: ")
            value = input("Enter the value: ")
            insert_key_value(key, value)
        elif choice == "/get":
            key = input("Enter the key: ")
            value = get_value(key)
            if value:
                print(f"Value for key '{key}': {value}")
        elif choice == "/update":
            key = input("Enter the key: ")
            new_value = input("Enter the new value: ")
            update_value(key, new_value)
        elif choice == "/delete":
            key = input("Enter the key: ")
            delete_key(key)
        elif choice == "/all":
            display_all()
        elif choice == "/exit":
            break
        elif choice == "exit":
            print(markdown.Markdown("> Did you mean `/exit` ?"))
            print(" [bold red] >>> [/bold red] ", end="")
            if "yes".startswith(input().lower()):
                break
            else:
                continue
        elif choice == "/clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(markdown.Markdown(header_text, hyperlinks=True))

        elif choice == "/h":
            help_table = markdown.Table(title="[bold #9977aa] LINUX BOOK HELP [/bold #9977aa]")
            help_table.add_column("[bold #9977aa]COMMAND[/bold #9977aa]", style="bold ")
            help_table.add_column("[bold]DESCRIPTION[/bold]", style="italic #9977aa")
            help_table.add_row("/new", "Insert your own linux snippet", end_section=True)
            help_table.add_row("/get [#9977aa]--work[/#9977aa]", "What does this command do?", end_section=True)
            help_table.add_row("/get [#9977aa]--cmd[/#9977aa]", "Which command, is this work done by?", end_section=True)
            help_table.add_row("/update", "Update the value of a key", end_section=True)
            help_table.add_row("/delete", "Delete a key-value pair", end_section=True)
            help_table.add_row("/all", "Display all key-value pairs", end_section=True)
            help_table.add_row("/exit", "Exit the program", end_section=True)
            help_table.add_row("/clear", "Clear the screen", end_section=True)
            help_table.add_row("/h", "Show this help message", end_section=True)
            print(help_table)

        else:
            print("Invalid choice. Please try again.")

# Initiating entry point
if __name__ == "__main__":
    entry_point()

# Close the database connection
conn.close()

# Close the database connection
conn.close()
