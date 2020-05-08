import argparse
import os
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Open docs hosted on updoc. The URL to the updoc host should be stored in an environment variable 
    named `UPDOC_HOST`. 
    """)

    parser.add_argument("-l", "--language", help="Language of package")
    parser.add_argument("package", help="Package whose documentation to open")

    args = parser.parse_args()

    open_docs(package=args.package, language=args.language, host=os.environ['UPDOC_HOST'])