# coding=utf-8
"""
basic tests
"""
import os
import docopt
from find_known_secrets import main

import find_known_secrets.__version__ as v1
import find_known_secrets.__main__ as dunder_main

def test_version():
    print(v1)

def test_dunder_main():
    dir(dunder_main)

def test_this():
    here = os.path.abspath(os.path.dirname(__file__))
    PROJECT = "sample_lib"
    SRC = here + "/../sample_src/"
    main.go(here + "/../")

def test_docops():
    try:
        main.process_docopts()
    except docopt.DocoptExit:
        pass
