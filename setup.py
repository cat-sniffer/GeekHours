""" Build script for setuptools """

# pylint: disable=C0103,W0122

from pathlib import Path
from setuptools import find_packages, setup

base_dir = Path.cwd()
__pkginfo__ = {}

with open(str(base_dir.joinpath('geekhours/__pkginfo__.py'))) as f:
    exec(f.read(), __pkginfo__)

pkginfo_name = __pkginfo__['name']
pkginfo_version = __pkginfo__['version']
pkginfo_license = __pkginfo__['license_']
pkginfo_author = __pkginfo__['author']
pkginfo_author_email = __pkginfo__['author_email']
pkginfo_url = __pkginfo__['url']
pkginfo_maintainer = __pkginfo__['maintainer']
pkginfo_scripts = __pkginfo__['scripts']
pkginfo_platforms = __pkginfo__['platforms']
pkginfo_python_requires = __pkginfo__['python_requires']
pkginfo_classifiers = __pkginfo__['classifiers']
pkginfo_description = __pkginfo__['description']
pkginfo_long_description = __pkginfo__['long_description']

setup(
    name=pkginfo_name,
    version=pkginfo_version,
    license=pkginfo_license,
    description=pkginfo_description,
    long_description=pkginfo_long_description,
    long_description_content_type='text/markdown',
    author=pkginfo_author,
    author_email=pkginfo_author_email,
    url=pkginfo_url,
    maintainer=pkginfo_maintainer,
    scripts=pkginfo_scripts,
    platforms=pkginfo_platforms,
    python_requires=pkginfo_python_requires,
    classifiers=pkginfo_classifiers,
    packages=find_packages(),
)
