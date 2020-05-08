import webbrowser

import click

from .cli import cli
from .utils import _build_pkg_url


@cli.command("open")
@click.option(
    '--host', 'host',
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
    "package",
    type=str,
    required=True
)
def open_docs(host: str, category: str, package: str):
    """
    Open docs hosted on updoc

    Arguments: \n
        package            Package whose documentation to open [required]
    """
    url = _build_pkg_url(
        host=host,
        category=category, 
        pkg_name=package
    )
    webbrowser.open_new_tab(url=url)
