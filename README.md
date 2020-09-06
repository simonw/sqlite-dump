# sqlite-dump

[![PyPI](https://img.shields.io/pypi/v/sqlite-dump.svg)](https://pypi.org/project/sqlite-dump/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-dump?label=changelog)](https://github.com/simonw/sqlite-dump/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-dump/blob/master/LICENSE)

An improved version of .iterdump() for sqlite3

## Installation

Install this plugin using `pip`:

    $ pip install sqlite-dump

## Usage

Usage instructions go here.

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd sqlite-dump
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
