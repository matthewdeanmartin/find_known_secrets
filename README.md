# find_known_secrets
Scan for known secrets in your source code before you check in

badges
------
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE) ![Read the Docs](https://img.shields.io/readthedocs/pip.svg) ![Travis](https://travis-ci.com/matthewdeanmartin/jiggle_version.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/matthewdeanmartin/find_known_secrets/badge.svg?branch=master)](https://coveralls.io/github/matthewdeanmartin/find_known_secrets?branch=master) [![BCH compliance](https://bettercodehub.com/edge/badge/matthewdeanmartin/find_known_secrets?branch=master)](https://bettercodehub.com/)

Three Ways to Detect Secrets
----------
Pattern detection - use grep to find words like "password". git-secrets does this as well as pylint.

High entropy detection - detect-secrets does this.

Search for known secrets - Some secrets are found in conventional locations, such as AWS keys. They are typically key value pairs. As far as I known, this is a novel approach as of July 2018. So I wrote one.

All three approaches have different failure profiles.






