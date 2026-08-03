from urllib.parse import urlparse

def patchURL(originalCode, origin, fullURL):
    patchedCode = originalCode

    originParsed = urlparse(origin)
    fullParsed = urlparse(fullURL)

    replacements = {
        "window.location.origin": f"'{origin}'",
        "self.location.origin": f"'{origin}'",
        "location.origin": f"'{origin}'",

        "window.location.href": f"'{fullURL}'",
        "self.location.href": f"'{fullURL}'",
        "location.href": f"'{fullURL}'",

        "window.location.host": f"'{originParsed.netloc}'",
        "self.location.host": f"'{originParsed.netloc}'",
        "location.host": f"'{originParsed.netloc}'",

        "window.location.hostname": f"'{originParsed.hostname or ''}'",
        "self.location.hostname": f"'{originParsed.hostname or ''}'",
        "location.hostname": f"'{originParsed.hostname or ''}'",

        "window.location.protocol": f"'{originParsed.scheme}:'",
        "self.location.protocol": f"'{originParsed.scheme}:'",
        "location.protocol": f"'{originParsed.scheme}:'",

        "window.location.port": f"'{originParsed.port or ''}'",
        "self.location.port": f"'{originParsed.port or ''}'",
        "location.port": f"'{originParsed.port or ''}'",

        "window.location.pathname": f"'{fullParsed.path}'",
        "self.location.pathname": f"'{fullParsed.path}'",
        "location.pathname": f"'{fullParsed.path}'",

        "window.location.search": f"'{('?' + fullParsed.query) if fullParsed.query else ''}'",
        "self.location.search": f"'{('?' + fullParsed.query) if fullParsed.query else ''}'",
        "location.search": f"'{('?' + fullParsed.query) if fullParsed.query else ''}'",

        "window.location.hash": f"'#{fullParsed.fragment}'" if fullParsed.fragment else "''",
        "self.location.hash": f"'#{fullParsed.fragment}'" if fullParsed.fragment else "''",
        "location.hash": f"'#{fullParsed.fragment}'" if fullParsed.fragment else "''",

        "document.location.origin": f"'{origin}'",
        "document.location.href": f"'{fullURL}'",
    }

    if False: # set this to true if you want but this whole patch is problematic
        for old in sorted(replacements, key=len, reverse=True):
            patchedCode = patchedCode.replace(old, replacements[old])

    return patchedCode