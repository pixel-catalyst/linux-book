import pickle
import re

from rich import markdown
import json
from rich import print

from classes.database_controller import DatabaseController

error_catchers = json.load(open("./errors_catcher.json", "r"))
listen_to_commands = True
error_listener: str = "default listener"
settings: dict = {"listen_to_commands": False}


def load_settings():
    try:
        global settings
        settings = pickle.load(open("settings.bin", "rb"))
    except Exception as e:
        # print("Hmmm... seems to be your first time using this CLI :)\n let's configure some settings first")
        print("Should I learn from your mistakes? you can change it later\n >> ", end="")
        if input() == "y":
            settings = {
                "listen_to_commands": True
            }
        else:
            settings = {
                "listen_to_commands": False
            }
        pickle.dump(settings, open("settings.bin", "wb"))


load_settings()


def update_settings():
    pickle.dump(settings, open("settings.dat", "wb"))
    print("[green][ ✓ ][/green] [#888888]Settings saved[/#888888]")


class CommandProcessor:
    command: str = ""
    prefix: str = ""
    came_from_correction: bool = False

    def test_error_listener(self):
        # print("Testing error listener : ", listener)
        if error_listener != "":
            # print( f"\n[#aa88ff][ · ][/#aa88ff] [#888888]You previously typed {error_listener}, was it meant
            # to do what you did just now?[/#888888]")
            print("\n[#aa88ff][ · ][/#aa88ff] [#888888]I am trying to learn from you...[/#888888]")
            print(
                f"[#aa88ff][ · ][/#aa88ff] [#888888]You previously typed `{error_listener}`, did it mean the same as `{self.prefix}`? : [/#888888]",
                end="")
            if input() == "y":
                print("\n [blue]>>[/blue] Enter error remarks ( reason ) : ", end="")
                err_type = input()
                print(" [blue]>>[/blue] Enter suggestions to correct it : ", end="")
                corr = input()

                with open("errors_catcher.json", "r") as f:
                    old_error_catchments: dict = json.load(f)
                new_error_catchment = {
                    error_listener: {
                        "value": self.prefix,
                        "error_type": err_type,
                        "correction": corr
                    }
                }
                old_error_catchments.update(new_error_catchment)
                json.dump(old_error_catchments, open("errors_catcher.json", "w"))
                print("[green][ ✓ ][/green] [#888888]Added to dictionary[/#888888]")

    @staticmethod
    def __print_help(self):
        help_table = markdown.Table(title="[bold #9977aa] LINUX BOOK HELP [/bold #9977aa]")
        help_table.add_column("[bold #9977aa]COMMAND[/bold #9977aa]", style="bold ")
        help_table.add_column("[bold]DESCRIPTION[/bold]", style="italic #9977aa")
        help_table.add_row("/new [#9977aa]--key=<key> --val=<value>[/#9977aa]", "Insert your own linux snippet",
                           end_section=True)
        help_table.add_row("/get [#9977aa]--work[/#9977aa]", "What does this command do?", end_section=True)
        help_table.add_row("/get [#9977aa]--cmd[/#9977aa]", "Which command, is this work done by?", end_section=True)
        help_table.add_row("/update", "Update the value of a key", end_section=True)
        help_table.add_row("/delete", "Delete a key-value pair", end_section=True)
        help_table.add_row("/all", "Display all key-value pairs", end_section=True)
        help_table.add_row("/exit", "Exit the program", end_section=True)
        help_table.add_row("/clear", "Clear the screen", end_section=True)
        help_table.add_row("/learn", "Toggle learning from your mistakes", end_section=True)
        help_table.add_row("/h", "Show this help message", end_section=True)
        print(help_table)

    def set_expression(self, expression: str = "none"):
        """sets the given expression for this class object"""
        self.command = expression

    def get_expression(self) -> str:
        return self.command

    def interpret_command(self):
        self.prefix = self.command.split(" ")[0].strip()
        if self.command.startswith("/h"):
            self.__print_help(self)

        elif self.command.startswith("/all"):
            db_controller = DatabaseController()
            keys = db_controller.get_all_keys()
            print(keys)

        elif self.command.startswith("/clear"):
            print("\033c")

        elif self.command.startswith("/exit"):
            print("\n[green][ ✓ ][/green] Bye :)")
            quit(0)

        elif self.command.startswith("/get"):
            try:
                self.command = self.command.removeprefix("/get").strip()
                db_controller = DatabaseController()
                db_controller.ensure_existing()

                if self.command.startswith("--work"):
                    print(db_controller.get_value(self.command.removeprefix("--work").strip()))
                elif self.command.startswith("--cmd"):
                    print(db_controller.get_key_by_value(self.command.removeprefix("--cmd").strip()))
                else:
                    print("\n[red][ ⨯ ][/red] Unknown argument usage")

            except IndexError as e:
                print(
                    "\n[red][ ⨯ ][/red] Please provide some argument as well. \n      [#888888]Type `/h` for help[/#888888]")

        elif self.command.startswith("/new"):
            self.command = self.command.removeprefix("/new").strip()
            key_start, val_start = self.command.find("--key="), self.command.find("--val=")
            key = self.command[key_start + 6: val_start].strip()
            val = self.command[val_start + 6: len(self.command)].strip()

            print(f"identified key = {key} and val = {val}")

            if key == "" or val == "":
                print("One or more empty values passed")
                return

            db_controller = DatabaseController()
            db_controller.ensure_existing()
            db_controller.insert_new_pair(key, val)
            print("\n[green][ ✓ ][/green] New pair added")
            self.test_error_listener()

        elif self.command.startswith("/learn"):
            global settings
            settings["listen_to_commands"] = not settings["listen_to_commands"]
            update_settings()

        else:
            self.__handle_error(self.command)
            return

        if not self.came_from_correction: self.test_error_listener()
        self.came_from_correction = False

    def __handle_error(self, command: str):
        try:
            print("[red][ ⨯ ][/red] [#888888]Wrong command provided.[/#888888]")
            print("[#aa88ff][ · ][/#aa88ff] [#888888]Reason : [/#888888]",
                  f"[#888888]{error_catchers[command]['error_type']}[#/888888]")
            print("[#aa88ff][ · ][/#aa88ff] [#888888]Suggestion : [/#888888]",
                  f"[#888888]{error_catchers[command]['correction']}[/#888888]")
            print("\n[#aa88ff] >>[/#aa88ff] Correct the command to : ", f"{error_catchers[command]['value']}",
                  " ? [y/n] : ",
                  end="")
            if input() == "y":
                self.came_from_correction = True
                self.set_expression(error_catchers[command]["value"])
                self.interpret_command()
            else:
                print("\n[green][ ✓ ][/green] Command ignored")
        except KeyError:
            print("[red][ ⨯ ][/red] [#888888]Could not find any similar commands either[/#888888]")

            if settings["listen_to_commands"]:
                global error_listener
                error_listener = command
