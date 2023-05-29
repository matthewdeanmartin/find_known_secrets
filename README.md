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
