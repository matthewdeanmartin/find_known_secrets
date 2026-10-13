"""
basic tests
"""

import os

import docopt

import find_known_secrets.__main__ as dunder_main
import find_known_secrets.__version__ as v1
from find_known_secrets import main
from find_known_secrets.searcher import Searcher


def test_version():
    print(v1)


def test_dunder_main():
    dir(dunder_main)


def test_this():
    here = os.path.abspath(os.path.dirname(__file__))

    searcher = Searcher(here + "/../")
    searcher.run()


def test_docops():
    try:
        main.process_docopts()
    except docopt.DocoptExit:
        pass
