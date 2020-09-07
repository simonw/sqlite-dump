from setuptools import setup
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="sqlite-dump",
    description="An improved version of .iterdump() for sqlite3",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/sqlite-dump",
    project_urls={
        "Issues": "https://github.com/simonw/sqlite-dump/issues",
        "CI": "https://github.com/simonw/sqlite-dump/actions",
        "Changelog": "https://github.com/simonw/sqlite-dump/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["sqlite_dump"],
    install_requires=[],
    extras_require={"test": ["pytest", "sqlite-utils"]},
    tests_require=["sqlite-dump[test]"],
)
