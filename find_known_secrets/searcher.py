"""
3 ways to find secrets I know of:

- grep for THING = "xyzzy" and the like. dodgy and pylint does this.
- search for high entropy strings. detect-secrets does this.
- look up known secrets, e.g. values from an known .ini file, or values
  currently set in the environment

"""
import glob
import os
import sys
from typing import Optional

import tabulate
from colorama import Back, Fore, Style, init

init(autoreset=True)  # cross plat now


class Searcher:
    """Look for possible secrets from common ini, config files"""

    def __init__(self, source: str, files: Optional[str] = None) -> None:
        """Set up initial state"""
        self.source = source

        self.files = ["~/.aws/credentials"]
        if files:
            for file in files.split(","):
                self.files.append(file)

        # TODO: merge in more .ini files

        self.false_positives = ["localhost", "admin", "0.0.0.0"]

        self.skip_files: list[str] = []
        # TODO: merge in an ignore file

        self.secrets: list[str] = []

        self.found: dict[str, list[tuple[str, str]]] = {}

    def append_known_secrets(self) -> None:
        """
        Read key-value pair files with secrets. For example, .conf and .ini files.
        """
        for file_name in self.files:
            if "~" in file_name:
                file_name = os.path.expanduser(file_name)
            if not os.path.isfile(file_name):
                print("Don't have " + Back.BLACK + Fore.YELLOW + file_name + ", won't use.")
                continue
            with open(os.path.expanduser(file_name), encoding="utf-8") as file:
                for line in file:
                    if line and "=" in line:
                        possible = line.split("=")[1].strip(" \"'\n")
                        if len(possible) > 4 and possible not in self.false_positives:
                            self.secrets.append(possible)

    def search_known_secrets(self) -> None:
        """
        Search a path for known secrets, outputting text and file when found
        """
        count = 0
        here = os.path.abspath(self.source)

        for file in glob.glob(here + "/" + "**/*.*", recursive=True):
            if os.path.isdir(file):
                continue
            with open(file, encoding="utf-8") as file_handle:
                try:
                    contents = file_handle.read()
                except UnicodeDecodeError:
                    continue
                except Exception as exception:
                    print(exception)
                    print(file)
                    raise
            for secret in self.secrets:
                if secret in contents:
                    for line in contents.split("\n"):
                        if secret in line:
                            self.found.setdefault(file, []).append(
                                (
                                    secret,
                                    line.replace(
                                        secret,
                                        Fore.RED + Back.YELLOW + secret + Style.RESET_ALL,
                                    ),
                                )
                            )
                            count += 1

    def report(self) -> None:
        """Summarize findings"""
        current_directory = os.getcwd()
        count = len(self.found)
        if count > 0:
            print(Fore.RED + f"Found {count} secrets. Failing this run.")

            data = [
                (
                    key.replace(current_directory, ""),
                    tabulate.tabulate(tabular_data=value, tablefmt="plain"),
                )
                for key, value in self.found.items()
            ]
            result = tabulate.tabulate(
                tabular_data=data,
                headers=("File", "Secret Found - Secret Text"),
                tablefmt="grid",
            )
            print(result)

            sys.exit(-1)
        else:
            print("No known secrets found. Consider trying out detect-secrets and git-secrets, too.")

    def run(self) -> None:
        """
        Entry point method
        """
        self.append_known_secrets()
        self.search_known_secrets()
        self.report()


if __name__ == "__main__":
    searcher = Searcher("")
    searcher.run()
