import re
from urllib.parse import quote, urljoin


def rewriteCSS(css, base, proxy_route="proxy"):
    prefix = f"/{proxy_route.strip('/')}/"

    def replace(match):
        quote_char = match.group(1) or ""
        url = match.group(2).strip()

        if not url or url.startswith(("data:", "http://", "https://", "#", "mailto:", "tel:")):
            return match.group(0)

        full_url = urljoin(base, url)
        encoded_url = quote(full_url, safe="/:?&=#%")

        return f"url({quote_char}{prefix}{encoded_url}{quote_char})"

    return re.sub(r"url\((['\"]?)(.*?)\1\)", replace, css)