""" geekhours packaging information """

# pylint: disable=C0103

name = 'geekhours'
version = '0.0.1'
license_ = 'MIT'
author = 'Yukie Kato'
author_email = 'yukie.kato.28@gmail.com'
url = 'https://github.com/YukieK/GeekHours.git'
maintainer = 'Mitz Amano'
scripts = ['bin/geekhours']
platforms = 'Linux'
python_requires = '~=3.5'
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Environment :: Console',
    'Operating System :: POSIX :: Linux',
]
description = 'Study time management tool'

with open('README.md', 'r') as fh:
    # pylint: disable=C0103
    long_description = fh.read()
