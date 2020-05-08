def _format_host(host: str) -> str: 
    return host + "/" if host[-1] != "/" else host 


def _build_pkg_url(host: str, category: str, pkg_name: str) -> str: 
    # return f'{host}static/{category}/{pkg_name}/index.html'
    return (
        _format_host(host)          # e.g. https://docs.your_company.com
        + 'static/'                 # updoc format 
        + category.title() + '/'    # typically language, e.g. Python or R 
        + pkg_name + '/'            # package name 
        + 'index.html'              # updoc format, doc's index.html is entry pt 
    )
