import argparse
import os
import webbrowser

import click

from .cli import cli
from .utils import _build_pkg_url


@cli.command("open")
@click.option(
    '-h', '--host', 'host',
    envvar='UPDOC_HOST',
    type=str,
    required=True,
    is_flag=False,
    help='URL where updoc is hosted'
)
@click.option(
    '-l', '--language' '-c', '--category', 'category',
    is_flag=False,
    type=str,
    required=True,
    help="Language of package, e.g. `r` or `python`"
)
@click.argument(
    "pkg_name",
    type=str
)
def open_docs(host: str, category: str, pkg_name: str):
    """
    Open docs hosted on updoc

    Arguments: \n
        pkg_name            Package whose documentation to open [required]
    """
    url = _build_pkg_url(
        host=host,
        category=category, 
        pkg_name=pkg_name
    )
    webbrowser.open_new_tab(url=url)
