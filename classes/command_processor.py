from rich import markdown
import json
from rich import print

from classes.database_controller import DatabaseController

error_catchers = json.load(open("errors_catcher.json", "r"))


class CommandProcessor:
    command: str = ""

    @staticmethod
    def __print_help(self):
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

    def set_expression(self, expression: str = "none"):
        """sets the given expression for this class object"""
        self.command = expression

    def get_expression(self) -> str:
        return self.command

    def interpret_command(self, interactive=False):
        if self.command.startswith("/h"):
            self.__print_help()

        elif self.command.startswith("/clear"):
            print("\033c")

        elif self.command.startswith("/exit"):
            exit()

        elif self.command.startswith("/get"):
            self.command = self.command.split(" ")[1].strip()
            db_controller = DatabaseController()
            db_controller.ensure_existing()
            db_controller.get_value(key=self.command)

        else:
            self.__handle_error(self.command)

    def __handle_error(self, command: str):
        try:
            error_catchers[command]
            print("Did you mean : ", f"`{error_catchers[command]}`", " ?")
        except KeyError:
            print("Invalid command :(")
