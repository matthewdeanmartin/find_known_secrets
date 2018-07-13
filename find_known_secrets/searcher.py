# coding=utf-8
"""
3 ways to find secrets I know of:

- grep for THING = "xyzzy" and the like. dodgy and pylint does this.
- search for high entropy strings. detect-secrets does this.
- look up known secrets, e.g. values from an known .ini file, or values
  currently set in the environment

"""
from typing import List

import glob
import os

files = ["~/.aws/credentials"]

# TODO: merge in more .ini files

false_positives = ["localhost", "admin", "0.0.0.0"]

skip_files = []  # type: List[str]
# TODO: merge in an ignore file

secrets = []  # type: List[str]


def append_known_secrets(source, debug=False):  # type: (str, bool) -> None
    """
    Read key-value pair files with secrets. For example, .conf and .ini files.
    :return:
    """
    for file_name in files:
        if not os.path.isfile(file_name):
            print("Don't have " + file_name + ", won't use.")
            continue
        with open(os.path.expanduser(file_name), "r") as file:
            for line in file:
                if line and "=" in line:
                    possible = line.split("=")[1].strip(" \"'\n")
                    if len(possible) > 4 and possible not in false_positives:
                        secrets.append(possible)

    print(secrets)


def search_known_secrets(source, debug=False):  # type: (str, bool) -> None
    """
    Search a path for known secrets, outputing text and file when found
    :return:
    """
    count = 0
    here = os.path.abspath(source)
    for file in glob.glob(here + "/" + "**/*.*", recursive=True):
        print(file)
        if os.path.isdir(file):
            continue
        with open(file) as f:
            try:
                contents = f.read()
            except UnicodeDecodeError:
                # print("Can't read "+ file)
                continue
            except Exception as e:
                print(file)
                raise
        for secret in secrets:
            if secret in contents:
                print(file)
                print("-----------")
                for line in contents.split("\n"):
                    if secret in line:
                        print(secret, line)
                        count += 1

        if count > 0:
            print("Found {0} secrets. Failing this run.".format(count))
        else:
            print(
                "No known secrets found. Consider trying out detect-secrets and git-secrets, too."
            )


def go(source, debug=False):  # type: (str, bool) -> None
    """
    Entry point method
    :return:
    """
    append_known_secrets(source, debug)
    search_known_secrets(source, debug)


if __name__ == "__main__":
    go("", True)
