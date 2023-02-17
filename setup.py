import pathlib

from setuptools import setup, find_packages

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name='aye',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AntonZelenin/ayeyarwady",
    author="Anton Zelenin",
    packages=find_packages(),
    version='1.0.0'
)
