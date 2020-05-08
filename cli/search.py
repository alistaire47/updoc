import re
import requests
from typing import Dict

import click

from .cli import cli


def fetch_table_of_contents(host: str) -> Dict[str, Dict[str, str]]: 
    """
    Fetch the table of contents from the host homepage 

    :param host: URL of updoc host
    :return: Table of contents of all documentations available on the host 
    """
    # get table of contents 
    # home_endpt = f'{host}/available'
    home_endpt = host + '/available'
    res = requests.get(home_endpt)
    table_of_contents = res.json() 
    return {
        item['category']: {
            doc['doc_name']: doc['doc_path'] 
            for doc in item['documents']
        }
        for item in table_of_contents
    }


@cli.command('search')
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
    required=False,
    help="Language of package, e.g. `r` or `python`"
)
@click.argument(
    "package",
    type=str,
    required=False,
    default='.*'
)
def package_search(host: str, category: str, package: str = '.*') -> Dict[str, str]:
    """
    Search for available packages

    Arguments: \n
        package            Package whose documentation to open [required]
    """
    toc = fetch_table_of_contents(host=host)

    if category is None:
        # list matching packages for all categories on updoc host
        pkg_urls = dict()
        for cat in toc.keys():
            packages = [p for p in toc[cat.title()] if re.search(package, p)]
            pkg_urls[cat] = {p: host + toc[cat.title()][p] for p in packages}
    else:
        # list a documentation's full URL on updoc host
        if category.title() not in toc:
            raise ValueError('Invalid category')

        packages = [p for p in toc[category.title()] if re.search(package, p)]
        pkg_urls = {p: host + toc[category.title()][p] for p in packages}

    print(pkg_urls)
    return pkg_urls
