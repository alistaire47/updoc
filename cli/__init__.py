from cli.cli import cli
from cli.open import open_docs
from cli.search import package_search
from cli.version import package_version


__all__ = [
    "cli",
    "package_search",
    "package_version",
    "open_docs"
]