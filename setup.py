# coding=utf-8
# !/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

import codecs
import os
import sys
from distutils.core import setup, Command
from shutil import rmtree

from setuptools import find_packages  # , setup, Command

PROJECT_NAME = "find_known_secrets"

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()
about = {}
with open(os.path.join(here, PROJECT_NAME, "__version__.py")) as f:
    exec(f.read(), about)
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()
required = [
    'docopt'
]


class UploadCommand(Command):
    """Support setup.py publish."""
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass
        except OSError:
            pass

        self.status('Building Source distribution…')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Not uploading to PyPi, not tagging github…')
        self.status('Uploading the package to PyPi via Twine…')

        os.system('twine upload dist/*')
        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')
        sys.exit()

setup(
    name=PROJECT_NAME,
    version=about['__version__'],
    description='Find secrets in your source code using lists of secrets you already know',
    long_description=long_description,
    # markdown is not supported. Easier to just convert md to rst with pandoc
    # long_description_content_type='text/markdown',
    author='Matthew Martin',
    author_email='matthewdeanmartin@gmail.com',
    url='https://github.com/matthewdeanmartin/' + PROJECT_NAME,
    packages=find_packages(exclude=['test']),
    entry_points={

        'console_scripts': [
            'find_known_secrets=find_known_secrets.main:process_docopts',
        ]
    },
    install_requires=required,
    extras_require={},
    include_package_data=True,
    license='MIT',
    keywords="version, build tools",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    cmdclass={'upload': UploadCommand, },
    # setup_cfg=True,
    setup_requires=['pbr'
                    ],
    pbr=False
)
