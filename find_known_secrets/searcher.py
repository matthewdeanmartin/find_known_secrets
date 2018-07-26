# coding=utf-8
"""
3 ways to find secrets I know of:

- grep for THING = "xyzzy" and the like. dodgy and pylint does this.
- search for high entropy strings. detect-secrets does this.
- look up known secrets, e.g. values from an known .ini file, or values
  currently set in the environment

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import tabulate
import os
from typing import List, Tuple, Optional, Set, Dict


from colorama import init, Fore, Back, Style

_ = List

try:
    import configparser
except ImportError:
    # Python 2.x fallback
    import ConfigParser as configparser

import sys

if sys.version_info.major == 3:
    unicode = str


init(autoreset=True)  # cross plat now


class Searcher(object):
    def __init__(self, source, files=None):  # type: (str,Optional[str]) -> None
        self.source = source

        self.files = ["~/.aws/credentials"]
        if files:
            for file in files.split(","):
                self.files.append(file)

        # TODO: merge in more .ini files

        self.false_positives = ["localhost", "admin", "0.0.0.0"]

        self.skip_files = []  # type: List[str]
        # TODO: merge in an ignore file

        self.secrets = []  # type: List[str]

        self.found = {}  # type: Dict[str, List[Tuple[str,str]]]

    def append_known_secrets(self):  # type: () -> None
        """
        Read key-value pair files with secrets. For example, .conf and .ini files.
        :return:
        """
        for file_name in self.files:
            if "~" in file_name:
                file_name = os.path.expanduser(file_name)
            if not os.path.isfile(file_name):
                print(
                    "Don't have "
                    + Back.BLACK
                    + Fore.YELLOW
                    + file_name
                    + ", won't use."
                )
                continue
            with open(os.path.expanduser(file_name), "r") as file:
                for line in file:
                    if line and "=" in line:
                        possible = line.split("=")[1].strip(" \"'\n")
                        if len(possible) > 4 and possible not in self.false_positives:
                            self.secrets.append(possible)

    def search_known_secrets(self):  # type: () -> None
        """
        Search a path for known secrets, outputing text and file when found
        :return:
        """
        count = 0
        here = os.path.abspath(self.source)
        # python 3 only!
        # for file in glob.glob(here + "/" + "**/*.*", recursive=True):

        # py 2
        matches = []
        for root, dirnames, filenames in os.walk(here + "/"):
            for filename in filenames:
                matches.append(os.path.join(root, filename))

        for file in matches:
            if os.path.isdir(file):
                continue
            with open(file) as f:
                try:
                    contents = f.read()
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(e)
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
                                        Fore.RED
                                        + Back.YELLOW
                                        + secret
                                        + Style.RESET_ALL,
                                    ),
                                )
                            )
                            count += 1

    def report(self):  # type: ()-> None
        current_directory = os.getcwd()
        count = len(self.found)
        if count > 0:
            print(Fore.RED + "Found {0} secrets. Failing this run.".format(count))

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

            exit(-1)
        else:
            print(
                "No known secrets found. Consider trying out detect-secrets and git-secrets, too."
            )

    def go(self):  # type: () -> None
        """
        Entry point method
        :return:
        """
        self.append_known_secrets()
        self.search_known_secrets()
        self.report()


if __name__ == "__main__":
    searcher = Searcher("")
    searcher.go()
