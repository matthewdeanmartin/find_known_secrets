# coding=utf-8
"""
Find Known Secrets. Are you about to check in passwords and keys into your source control and lose your job?

Usage:
  find_known_secrets here
  find_known_secrets --source=<source> [--debug=<debug>]
  find_known_secrets -h | --help
  find_known_secrets --version

Options:
  --source=<source>  Source folder. e.g. src/
  -h --help     Show this screen.
  --version     Show version.
  --debug=<debug>  Show diagnostic info [default: False].
"""

import os
import logging
from docopt import docopt

from find_known_secrets.searcher import go

logger = logging.getLogger(__name__)


def process_docopts():
    # type: ()->None
    """
    Take care of command line options
    """
    arguments = docopt(__doc__, version="Jiggle Version 1.0")
    logger.debug(arguments)
    if arguments["here"]:
        go(source="", debug=arguments["--debug"])
    else:
        go(source=arguments["--source"], debug=arguments["--debug"])


if __name__ == "__main__":
    process_docopts()
