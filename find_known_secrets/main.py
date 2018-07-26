# coding=utf-8
"""
Find Known Secrets. Are you about to check in passwords and keys into your public source control and lose your job?

Usage:
  find_known_secrets here
  find_known_secrets [--source=DIR] --secrets=<ini>
  find_known_secrets -h | --help
  find_known_secrets --version

Options:
  --secrets=<secrets> List of ini or ini-like files with known secrets
  --source=DIR        Source folder. e.g. src/ [default: .]
  -h --help           Show this screen.
  --version           Show version.
  --debug=<debug>     Show diagnostic info [default: False]
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from docopt import docopt

from find_known_secrets.searcher import Searcher
from find_known_secrets.__version__ import __version__

logger = logging.getLogger(__name__)


def go():  # type: () -> None
    """
    Default scenario
    """
    searcher = Searcher(source="")
    searcher.go()


def process_docopts():  # type: ()->None
    """
    Take care of command line options
    """

    arguments = docopt(__doc__, version="Find Known Secrets {0}".format(__version__))

    logger.debug(arguments)
    # print(arguments)
    if arguments["here"]:
        # all default
        go()
    else:
        # user config
        files = arguments["--secrets"]

        searcher = Searcher(source=arguments["--source"], files=files)
        searcher.go()


if __name__ == "__main__":
    process_docopts()
