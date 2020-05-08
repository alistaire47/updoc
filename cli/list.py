import argparse
import os
import requests
import sys
from bs4 import BeautifulSoup 
from typing import Dict

from .utils import _build_pkg_url


def fetch_pkg_version(pkg_url: str, category: str) -> str: 
    """
    Find the version of package documentation 

    :param pkg_url: Full URL of package documentation 
    :param category: If ``pkg_name`` has docs in multiple languages, 
        the language for which to get docs.
    :return: version string of the package requested 
    """
    # default HTML parsing arguments
    VERSION_TAG = {
        # assuming pkgdown for R 
        'r': {
            'name': 'span', 
            'class_': 'label label-default'
        }, 
        # assuming readthedocs style for Python 
        'python': {
            'name': 'div', 
            'class_': 'version'
        }
    }
    # fetch the page and parse version 
    page = requests.get(pkg_url) 
    soup = BeautifulSoup(page.content, 'html.parser')
    version = soup.find_all(**VERSION_TAG[category.lower()])[0].get_text().strip()
    return str(version)


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


def _main(arg_list):
    parser = argparse.ArgumentParser(description="""
    Query information from updoc host. The URL to the updoc host should be 
    stored in an environment variable named `UPDOC_HOST`. 
    """)

    parser.add_argument("-c", "--category", help="Language of package, e.g. `r` or `python`")
    parser.add_argument("-p", "--package", help="Package whose documentation to open")
    parser.add_argument("-v", "--version", help="Query version of the package", action="store_true")

    args = parser.parse_args(arg_list)

    if args.category is None and args.package is None and not args.version: 
        # list all categories on updoc host 
        toc = fetch_table_of_contents(host=os.environ['UPDOC_HOST'])
        return list(toc.keys())
    elif args.category is not None and args.package is None and not args.version: 
        # list all documentations within a category on updoc host 
        toc = fetch_table_of_contents(host=os.environ['UPDOC_HOST'])
        if args.category in toc: 
            return list(toc[args.category].keys())
        else: 
            return 'Invalid category' 
    elif args.category is not None and args.package is not None and not args.version: 
        # list a documentation's full URL on updoc host 
        toc = fetch_table_of_contents(host=os.environ['UPDOC_HOST'])
        if args.category in toc and args.package in toc[args.category]: 
            pkg_url = _build_pkg_url(
                host=os.environ['UPDOC_HOST'], 
                category=args.category, 
                pkg_name=args.package
            )
            return pkg_url
        else: 
            return 'Requested package not found in the category'
    elif args.category is not None and args.package is not None and args.version: 
        # list the version of a package documentation on updoc host 
        version = fetch_pkg_version(
            pkg_url=_build_pkg_url(
                host=os.environ['UPDOC_HOST'], 
                category=args.category, 
                pkg_name=args.package
            ), 
            category=args.category
        )
        return version 


def _cli():
    _main(sys.argv[1:])


if __name__ == "__main__":
    _cli()
