# find_known_secrets
Scan for known secrets in your source code before you check in

badges
------

![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/find-known-secrets) [![Downloads](https://pepy.tech/badge/find_known_secrets/month)](https://pepy.tech/project/find-known-secrets/month)

Three Ways to Detect Secrets
----------
Pattern detection - use grep to find words like "password". git-secrets does this as well as pylint.

High entropy detection - detect-secrets does this.

Search for known secrets - Some secrets are found in conventional locations, such as AWS keys. They are typically key value pairs. As far as I known, this is a novel approach as of July 2018. So I wrote one.

All three approaches have different failure profiles.

## Project Links

- [GitHub](https://github.com/matthewdeanmartin/find_known_secrets)
- [PyPI](https://pypi.org/project/find-known-secrets/)
- [Bug Tracker](https://github.com/matthewdeanmartin/find_known_secrets/issues)
- [Change Log](https://github.com/matthewdeanmartin/find_known_secrets/blob/main/CHANGELOG.md)


## Python 3.15 verification — 2026-10-04

The former docopt dependency has no published wheel on any tested Python. Runtime now uses docopt-ng>=0.9,<1 with the same docopt import and CLI grammar. Eight tests pass on 3.15.0rc3 stable/pre and Python 3.14.7; subprocess tests use the interpreter being tested and isolate the operator's home credentials. Installed-wheel help and synthetic secret-found/clean scans pass. Full developer setup still has a PyYAML wheel blocker. This dependency change is worth a patch release; the current PyPI 1.3.0 still requires docopt.

Dependencies were installed only from published wheels; the project's own pure-Python wheel was built locally without build isolation. `uv lock --upgrade` refreshed the lock. No GitHub builds, releases or upstream reports were sent. Upstream bug filing is the human operator's job.
