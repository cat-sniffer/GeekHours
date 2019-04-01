""" Build script for setuptools """

from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    # pylint: disable=C0103
    long_description = fh.read()

setup(
    name='geekhours',
    version='0.0.1',
    author='Yukie Kato',
    author_email='yukie.kato.28@gmail.com',
    maintainer='Mitz Amano',
    description='Study time management tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/YukieK/GeekHours.git',
    license='MIT',
    packages=find_packages(),
    scripts=['bin/geekhours'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
    ],
    platforms='Linux',
    python_requires='~=3.5',
)
