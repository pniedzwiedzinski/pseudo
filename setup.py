#!/usr/bin/env python

from setuptools import setup, find_packages
import pseudo


def long_description():
    with open("README.md") as f:
        return f.read()


setup(
    name="pseudo",
    version=pseudo.__version__,
    author="Patryk Niedzwiedzinski",
    author_email="pniedzwiedzinski19@gmail.com",
    description="Pseudocode interpreter prototype",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["pdc=pseudo.cli:pdc"]},
    packages=find_packages(),
    tests_require=["pytest"],
    install_requires=["Click>=7.0"],
    url="https://github.com/pniedzwiedzinski/pseudo",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)

