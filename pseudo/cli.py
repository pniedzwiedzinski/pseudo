#!/usr/bin/env python


import sys
import click
import codecs

from pseudo import __version__, __doc__, compile
from pseudo.run import run


__author__ = "Patryk Niedźwiedziński"


@click.command()
@click.option("--version", "-v", help="Display version", is_flag=True)
@click.option(
    "--range-symbol",
    default="...",
    help="Set range symbol in for loop (default: '...')",
)
@click.argument("file", type=click.Path(exists=True), required=False)
def pdc(file, version, range_symbol):
    """Run pseudocode file."""

    if version:
        print(__version__)
        sys.exit()

    if file is None:
        click.echo('⚠️  Error: Missing argument "FILE".')
        sys.exit(1)

    with codecs.open(file, encoding="utf-8") as fp:
        text_input = fp.read()

    instructions = compile(text_input, range_symbol)
    run(instructions)
