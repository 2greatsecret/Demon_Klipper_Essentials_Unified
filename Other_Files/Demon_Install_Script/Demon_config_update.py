"""
requires:
    - rich : install using `python3 -m pip install rich`
    - configupdater : `python3 -m pip install ConfigUpdater`

"""

"""
usage: `python3 Demon_config_update.py`

positional arguments:
  none

optional arguments:
  none
"""

from configupdater import ConfigUpdater
import os
from pathlib import Path

# Python rich
from rich.console import Console
console = Console()

from rich.traceback import install
install(show_locals=False)

from rich import print
from rich.prompt import Prompt

# Paths to the configuration files
# TODO list all demon_user_settings_v#.#.#.cfg in the folder,
#  use the latest one,
#  then ask if this is the one the user wants to migrate,
#  continue in descending order of version,
#  If the last file is not accepted, print a joke saying the user should make-up his mind. and use the :exploding_head:
#OLD_CONFIG_PATH = "~/printer_data/config/Demon_User_files/Previous_versions/demon_user_settings_v2.9.4.cfg"
#NEW_CONFIG_PATH = "~/printer_data/config/Demon_User_files/demon_user_settings_v2.9.5_test.cfg"
OLD_CONFIG_PATH = os.path.expanduser("~/demon_user_settings_v2.9.4.cfg")
NEW_CONFIG_PATH = os.path.expanduser("~/demon_user_settings_v2.9.5_test.cfg")

# Function to load a configuration file
def load_config(file_path):
    updater = ConfigUpdater()
    updater.read(file_path)
    return updater


# Function to save a configuration file
def save_config(updater, file_path):
    with open(file_path, "w") as f:
        updater.write(f)


def ask_file_path():
    while True:
        # Prompt the user for the file path
        file_path = Prompt.ask("Please enter the full file path and name")

        # Validate the input (e.g., check if it's a valid path)
        path = Path(file_path)
        if path.parent.exists():
            return file_path
        else:
            print(f"[red]Invalid path:[/red] {file_path}. Please try again.")


# Function to compare and merge configurations
def compare_and_merge_configs(old_config, new_config, output_path):

    console.rule(f":exclamation: Informations :exclamation:")
    print(f":grey_exclamation: [blue]Old value[1] is the value from your config backup at {OLD_CONFIG_PATH}")
    print(f":grey_exclamation: [green]New value[1] is the value from the new config template already copied at {NEW_CONFIG_PATH}\n")

    # Iterate through all sections in the new config
    for section in new_config.sections():

        for key, item in new_config[section].items():
            if old_config.has_section(section) and old_config.has_option(section, key):
                old_value = old_config[section][key].value
                new_value = new_config[section][key].value

                if old_value != new_value and key != 'variable_demon_version':

                    # Prompt the user to choose the value
                    console.rule(f"Section: [yellow]\[{section}][/], key: [purple]{key}[/]")
                    print(f"[blue]\[1][/] Old value: [blue]{old_value}[/]")
                    print(f"[green]\[2][/] New value: [green]{new_value}[/]")

                    choice = Prompt.ask(
                        "Which value do you want to keep? [blue]\[1][/] or [green]\[2][/] or [red][q][/] to cancel and quit: ",
                        choices=["1", "2","q"],
                        default="2",
                    )

                    if choice == '1':
                        print(f"[blue]Old value[/] kept!\n")
                        new_config[section][key].value = old_value

                    elif choice == '2':
                        print(f"[green]New value[/] kept!\n")
                    
                    elif choice == 'q':
                        print(f"[red]Operation Cancelled, no file was written![/]\n")
                        exit()


    # Save the merged configuration
    console.rule(f"Save config")
    choice = Prompt.ask(
        f"Do you want to overwrite [purple]\"{output_path}\"[/]? ",
        choices=["y", "n", "q"],
        default="y",
    )

    if choice == 'n':
        output_path=ask_file_path()
    
    elif choice == 'q':
        print(f"[red]Operation Cancelled, no file was written![/]\n")
        exit()

    save_config(new_config, output_path)
    print(f"Merged configuration saved to [purple]\"{output_path}\"[/]\n")
    console.rule(f"")

# Main function
def main():
    # Ensure old configuration exists
    if not os.path.exists(OLD_CONFIG_PATH):
        print(f"Error: {OLD_CONFIG_PATH} does not exist.")
        return

    # Ensure new configuration exists
    if not os.path.exists(NEW_CONFIG_PATH):
        print(f"Error: {NEW_CONFIG_PATH} does not exist.")
        return

    # Load configurations
    old_config = load_config(OLD_CONFIG_PATH)
    new_config = load_config(NEW_CONFIG_PATH)

    # Compare and merge
    compare_and_merge_configs(old_config, new_config, NEW_CONFIG_PATH)

if __name__ == "__main__":
    main()
