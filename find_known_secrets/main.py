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

import logging

from docopt import docopt

from find_known_secrets.__version__ import __version__
from find_known_secrets.searcher import Searcher

logger = logging.getLogger(__name__)


def run() -> None:
    """
    Default scenario
    """
    searcher = Searcher(source="")
    searcher.run()


def process_docopts() -> None:
    """
    Take care of command line options
    """

    arguments = docopt(__doc__, version=f"Find Known Secrets {__version__}")

    logger.debug(arguments)
    if arguments["here"]:
        # all default
        run()
    else:
        # user config
        files = arguments["--secrets"]

        searcher = Searcher(source=arguments["--source"], files=files)
        searcher.run()


if __name__ == "__main__":
    process_docopts()
