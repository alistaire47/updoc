import argparse
import os
import sys
import webbrowser


def open_docs(package: str, language: str, host: str):
    """
    Open docs hosted on updoc

    :param package: String of package whose docs to open
    :param language: If ``package`` has docs in multiple languages, the language for which to get
        docs.
    :param host: URL of updoc host
    """
    if host[-1] != "/":
        host += "/"

    url = f"{host}static/{language.title()}/{package}/index.html"
    webbrowser.open_new_tab(url=url)


def _main(arg_list):
    parser = argparse.ArgumentParser(description="""
    Open docs hosted on updoc. The URL to the updoc host should be stored in an environment variable 
    named `UPDOC_HOST`. 
    """)

    parser.add_argument("-l", "--language", help="Language of package, e.g. `r` or `python`")
    parser.add_argument("package", help="Package whose documentation to open")

    args = parser.parse_args(arg_list)

    open_docs(package=args.package, language=args.language, host=os.environ['UPDOC_HOST'])


def _cli():
    _main(sys.argv[1:])


if __name__ == "__main__":
    _cli()
