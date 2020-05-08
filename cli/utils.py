def _format_host(host: str) -> str: 
    if host[-1] != "/":
        host += "/"
        
    return host


def _build_pkg_url(host: str, category: str, pkg_name: str) -> str: 
    """
    Assemble docs URL for package
    
    :param host: e.g. https://docs.your_company.com/ 
    :param category: typically language, e.g. Python or R 
    :param pkg_name: package name 
    """
    # return f'{host}static/{category}/{pkg_name}/index.html'
    return f"{_format_host(host)}static/{category.title()}/{pkg_name}/index.html"
