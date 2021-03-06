# Updoc

- [What's `UpDoc`?](#whats-updoc)
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [`UpDoc` Command-line Interface](#updoc-command-line-interface)

## What's `UpDoc`?

A self hosted readthedocs.io-like documentation repository and hosting service.  The problem that this attempts to 
solve is that there aren't many easy to use solutions to store and host simple static html.  There are numerous 
tools out there like Sphinx (for Python and many other languages), pkgdown and pkgnet (for R), and SchemaSpy (for 
databases) that generate beautiful html documentation.  This allows users to host that documentation in a central 
location and easily categorize and share it.

## Quick Start

1. Build the docker image

```
git clone https://github.com/uptake/updoc
cd updoc
docker build -t updoc .
```

2. Run the docker image

```
docker run --name doc --rm -d -p 8080:80 updoc
```

3: Visit in your browser

```
# On Mac
open http://localhost:8080
```

You're all set!

## Features

- **Ready**: Supports AWS S3 and file system storage out of the box.
- **Extensible**: We made it really easy to support other storage backends.
- **Web UI**: Allows you to easily search through and view hosted static html.

## Usage

### Posting documentation tarballs to **docserver**

The way in which a folder is tar'd for distribution on docserver is **important**.  In order for the application to
correctly understand which category your documentation belongs to and the name of your documentation, the naming
of your tarball must follow the following format: ``<CATEGORY>_<DOCNAME>.tar.gz``.  When extracted, the tarball must
expand into a single folder named ``<DOCNAME>``, containing at minimum a ``<DOCNAME>/index.html``.

You can host static html with ``docserver`` using a POST request:

```
# bash
tarball=<PATH-TO-TARBALL>
curl -X POST -F file=@$tarball http://localhost:8080
```

If all goes well, you should receive the this message:

```
Document: <DOCNAME> was correctly uploaded, stored, and extracted.
```

## Configuration

Documentation storage: By default, ``docserver`` uses file system storage, but in a production environment in most
cases S3 or another object store is desirable. ``docserver`` supports AWS S3 out of the box. The recommended way to
set configuration options is using a ``.env`` file:

```
# .env
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID_HERE>
AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY_HERE>
AWS_DEFAULT_REGION=<YOUR_PREFERED_REGION_HERE>
AWS_DEFAULT_BUCKET=<YOUR_PREFERRED_DEFAULT_BUCKET_HERE>
AWS_BUCKET_FOLDER_PATH=<YOUR_PATH_TO_S3_FOLDER_IN_BUCKET>
```

The environment file can then be sourced when running from docker:

```
docker run --name doc --rm -d -p 8080:80 --env-file=.env updoc
```

## `UpDoc` Command-line Interface

Some users may prefer interacting with `UpDoc` from a command-line environment (e.g. bash). We provide some features for this usage as well. To leverage `UpDoc` CLI, one needs to install using 
```bash 
python setup.py install updoc[cli]
```

### Terminology 

- `--category` (or `-c` in short): Documentations are grouped by `category`. We recommend assigning language (e.g. `Python`, `R`), workflow component (e.g. `Database`), or functional units (e.g. `Blog`) as `category`. 
- `--package` (or `-p` in short): We refer to each documentation entry as a `package` in the CLI. 
- `--version` (or `-v` in short): `version` is an experimental feature for `Python` package documentations using `readthedocs` style and `R` package documentations generated by `pkgdown`. It greps the version info from the HTML documentation sites. 

### Example Commands 

Set up the `UpDoc` hostname in your environment, e.g. 
```bash 
export UPDOC_HOST="https://docs.your_company.com/"
```

Open documentation of a package (e.g. `R` package `httr`)

```bash
updoc open --category r --package httr 
```

Search all categories with regex

```bash
updoc search ht.* 
```

Search all available documentations within a category (e.g. `Python` category)

```bash
updoc search -c python
```

Search a category of packages for matching names and print the full URL of the 
documentation of matching packages (you may want to use `updoc open` instead 
to open directly in browser)

```bash
updoc search -c r httr 
```

Prints the version of the documentation of a package (e.g. `Python` package `requests`)

```bash
updoc version --category python requests
```

---

That's all folks! If you find this project helpful, please consider giving us a star. If you have any comments or questions, please feel free to raise an [issue](https://github.com/uptake/updoc/issues). Contributions are greatly appreciated! 
