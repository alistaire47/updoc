import requests
from bs4 import BeautifulSoup

import click

from .cli import cli
from .utils import _build_pkg_url


def fetch_pkg_version(pkg_url: str) -> str:
    """
    Find the version of package documentation

    :param pkg_url: Full URL of package documentation
    :return: version string of the package requested
    """
    # fetch the page and parse version
    page = requests.get(pkg_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    version = soup.find_all(class_='version')[0].get_text().strip()
    return version


@cli.command('version')
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
    type=str
)
def package_version(host: str, category: str, package: str) -> str:
    """
    Query the current version of a package documentation hosted on updoc

    Arguments: \n
        package            Package whose documentation to open [required]
    """
    pkg_url = _build_pkg_url(
        host=host,
        category=category,
        pkg_name=package
    )

    version = fetch_pkg_version(pkg_url=pkg_url)

    print(version)
    return version
