import argparse
import os
import sys
import webbrowser

from .utils import _build_pkg_url


def open_docs(host: str, category: str, pkg_name: str):
    """
    Open docs hosted on updoc

    :param pkg_name: String of package whose docs to open
    :param category: If ``pkg_name`` has docs in multiple languages, 
        the language for which to get docs.
    :param host: URL of updoc host
    """
    url = _build_pkg_url(
        host=host, 
        category=category, 
        pkg_name=pkg_name
    )
    webbrowser.open_new_tab(url=url)


def _main(arg_list):
    parser = argparse.ArgumentParser(description="""
    Open docs hosted on updoc. The URL to the updoc host should be 
    stored in an environment variable named `UPDOC_HOST`. 
    """)

    parser.add_argument("-c", "--category", help="Language of package, e.g. `r` or `python`")
    parser.add_argument("-p", "--package", help="Package whose documentation to open")

    args = parser.parse_args(arg_list)

    open_docs(host=os.environ['UPDOC_HOST'], category=args.category, pkg_name=args.package)


def _cli():
    _main(sys.argv[1:])


if __name__ == "__main__":
    _cli()
