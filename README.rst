find_known_secrets
==================

Scan for known secrets in your source code before you check in

badges
------

|MIT licensed| |Read the Docs| |Build Status| |Coverage Status| |BCH
compliance|

Three Ways to Detect Secrets
----------------------------

Pattern detection - use grep to find words like “password”. git-secrets
does this as well as pylint.

High entropy detection - detect-secrets does this.

Search for known secrets - Some secrets are found in conventional
locations, such as AWS keys. They are typically key value pairs. As far
as I known, this is a novel approach as of July 2018. So I wrote one.

All three approaches have different failure profiles.

.. |MIT licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE
.. |Read the Docs| image:: https://img.shields.io/readthedocs/pip.svg
.. |Build Status| image:: https://travis-ci.com/matthewdeanmartin/find_known_secrets.svg?branch=master
   :target: https://travis-ci.com/matthewdeanmartin/find_known_secrets
.. |Coverage Status| image:: https://coveralls.io/repos/github/matthewdeanmartin/find_known_secrets/badge.svg?branch=master
   :target: https://coveralls.io/github/matthewdeanmartin/find_known_secrets?branch=master
.. |BCH compliance| image:: https://bettercodehub.com/edge/badge/matthewdeanmartin/find_known_secrets?branch=master
   :target: https://bettercodehub.com/
