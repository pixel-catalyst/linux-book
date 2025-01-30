"""
Error template
[red][ ⨯ ][/red] [#888888]  [/#888888]

Success Template
[green][ ✓ ][/green] [#888888] [/#888888]

Log Template
[#aa88ff][ · ][/#aa88ff] [#888888]  [/#888888]
"""

import pickle
from rich import markdown
import json
from rich import print

from classes.database_controller import DatabaseController

error_catchers = json.load(open("./resources/errors_catcher.json", "r"))
listen_to_commands = True
error_listener: str = "default listener"
settings: dict = {"listen_to_commands": False}


def load_settings():
    try:
        global settings
        settings = pickle.load(open("./resources/settings.bin", "rb"))
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
        global error_listener
        if error_listener != "default listener":
            # print( f"\n[#aa88ff][ · ][/#aa88ff] [#888888]You previously typed {error_listener}, was it meant
            # to do what you did just now?[/#888888]")
            print("\n[#aa88ff][ · ][/#aa88ff] [#888888]I am trying to learn from you...[/#888888]")
            print(
                f"[#aa88ff][ · ][/#aa88ff] [#888888]You previously typed `{error_listener}`, did it mean the same as `{self.command}`? : [/#888888]",
                end="")
            uinput = input()
            if uinput == "y":
                print("\n [blue]>>[/blue] Enter error remarks ( reason ) : ", end="")
                err_type = input()
                print(" [blue]>>[/blue] Enter suggestions to correct it : ", end="")
                corr = input()

                with open("./resources/errors_catcher.json", "r") as f:
                    old_error_catchments: dict = json.load(f)
                new_error_catchment = {
                    error_listener: {
                        "value": self.prefix,
                        "error_type": err_type,
                        "correction": corr
                    }
                }
                old_error_catchments.update(new_error_catchment)
                json.dump(old_error_catchments, open("./resources/errors_catcher.json", "w"))
                print("[green][ ✓ ][/green] [#888888]Learnt and added to dictionary :)[/#888888]")

            elif uinput == "n":
                error_listener = "default listener"
                print("[#aa88ff][ · ][/#aa88ff] [#888888]Appended to negation rules[/#888888]")

    @staticmethod
    def __print_help(self):
        help_table = markdown.Table(title="[bold #9977aa] LINUX BOOK HELP [/bold #9977aa]")
        help_table.add_column("[bold #9977aa]COMMAND[/bold #9977aa]", style="bold ")
        help_table.add_column("[bold]DESCRIPTION[/bold]", style="italic #9977aa")
        help_table.add_row("/new [#9977aa]--key --val[/#9977aa]", "Insert your own linux snippet",
                           end_section=True)
        help_table.add_row("/get [#9977aa]--work[/#9977aa]", "Get cmd that does this work", end_section=True)
        help_table.add_row("/get [#9977aa]--cmd[/#9977aa]", "Get work that this cmd does", end_section=True)
        help_table.add_row("/update [#9977aa]--where --new-val[/#9977aa]", "Update the cmd for a work", end_section=True)
        help_table.add_row("/delete <work>", "Delete a key-value pair", end_section=True)
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
            keys_table = markdown.Table(title="[bold #9977aa] ALL COMMANDS [/bold #9977aa]", title_style="bold")
            keys_table.add_column("[bold #9977aa]COMMAND[/bold #9977aa]", style="bold ")
            keys_table.add_column("[bold]DESCRIPTION[/bold]", style="italic #9977aa")
            if len(keys) > 0 :
                for key in keys:
                    keys_table.add_row(key, db_controller.get_value(key)[0][1], end_section=True)
                print(keys_table)
            else:
                print("No commands available")

        elif self.command.startswith("/delete"):
            db_controller = DatabaseController()
            try:
                db_controller.delete_pair(self.command.removeprefix("/delete").strip())
                print(f"\n[green][ ✓ ][/green] [#888888]Deleted {self.command.removeprefix('/delete').strip()}")
            except Exception as e:
                print("[red][ ⨯ ][/red] [#888888]No such keys found[/#888888]")

        elif self.command.startswith("/clear"):
            print("\033c")

        elif self.command.startswith("/exit"):
            print("\n[green][ ✓ ][/green] Bye :)")
            # quit(0)
            exit(0)

        elif self.command.startswith("/get"):
            try:
                self.command = self.command.removeprefix("/get").strip()
                db_controller = DatabaseController()
                db_controller.ensure_existing()

                if self.command.startswith("--work"):
                    keys = db_controller.get_value(self.command.removeprefix("--work").strip().removeprefix("=").strip())
                    keys_table = markdown.Table(title="[bold #9977aa] MATCHED COMMANDS [/bold #9977aa]", title_style="bold")
                    keys_table.add_column("[bold]WORK[/bold]", style="italic #9977aa")
                    keys_table.add_column("[bold #9977aa]COMMAND[/bold #9977aa]", style="bold ")
                    for key in keys:
                        keys_table.add_row(key[0], key[1], end_section=True)
                    print(keys_table)

                elif self.command.startswith("--cmd"):
                    keys = db_controller.get_key_by_value(self.command.removeprefix("--cmd").strip().removeprefix("=").strip())
                    keys_table = markdown.Table(title="[bold #9977aa] MATCHED COMMANDS [/bold #9977aa]", title_style="bold")
                    keys_table.add_column("[bold #9977aa]COMMAND[/bold #9977aa]", style="bold")
                    keys_table.add_column("[bold ]WORK[/bold ]", style="italic #9977aa")
                    for key in keys:
                        keys_table.add_row(key[1], key[0], end_section=True)
                    print(keys_table)

                else:
                    print("\n[red][ ⨯ ][/red] Bad / Missing Argument")

            except IndexError as e:
                print(
                    "\n[red][ ⨯ ][/red] Please provide some argument as well. \n      [#888888]Type `/h` for help[/#888888]")

        elif self.command.startswith("/new"):
            self.command = self.command.removeprefix("/new").strip()
            key_start, val_start = self.command.find("--key"), self.command.find("--val")
            key_end = val_start
            if val_start == -1:
                val_start = self.command.find("--value=")
                key_end = val_start
                val_start += 2
            key = self.command[key_start + 5: key_end].strip()
            val = self.command[val_start + 5: len(self.command)].strip()

            print(f"\n[#aa88ff][ · ][/#aa88ff] [#888888] identified KEY = {key} | VAL = {val} [/#888888] ")

            if key == "" or val == "":
                print("One or more empty values passed")
                return

            db_controller = DatabaseController()
            db_controller.ensure_existing()
            db_controller.insert_new_pair(key, val)
            print("[green][ ✓ ][/green] [#888888]New pair added[/#888888]")
            self.test_error_listener()

        elif self.command.startswith("/learn"):
            global settings
            settings["listen_to_commands"] = not settings["listen_to_commands"]
            update_settings()

        elif self.command.startswith("/update"):
            where_index, value_index = self.command.find("--where="), self.command.find("--new-val=")
            key = self.command [where_index+8: value_index].strip()
            value = self.command[value_index+10:].strip()

            if not "--where=" in self.command and "--new-val=" in self.command:
                print("[red][ ⨯ ][/red] [#888888] Bad / Missing Arguments [/#888888]")
                return

            if key=="" or value=="":
                print("[red][ ⨯ ][/red] [#888888] Empty Arguments [/#888888]")
                return

            try:
                dbc = DatabaseController()
                dbc.update_value(key, value)
                print(f"[#aa88ff][ · ][/#aa88ff] [#888888] Setting [[ {key} = {value} ]]... [/#888888]")
                print("[green][ ✓ ][/green] [#888888] Value Updated [/#888888]")

            except Exception as e:
                print("[red][ ⨯ ][/red] [#888888] Database Error, Could not update... [/#888888]")
                with open("dbLogs.txt", "w") as fe:
                    fe.write(str(e))

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
