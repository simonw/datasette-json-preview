from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-json-preview",
    description="Preview of new JSON default format for Datasette, see issue #782",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-json-preview",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-json-preview/issues",
        "CI": "https://github.com/simonw/datasette-json-preview/actions",
        "Changelog": "https://github.com/simonw/datasette-json-preview/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_json_preview"],
    entry_points={"datasette": ["json_preview = datasette_json_preview"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx", "sqlite-utils"]},
    tests_require=["datasette-json-preview[test]"],
)
