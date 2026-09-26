from flask import Flask, Response, request, send_from_directory
import flask.cli
from urllib.parse import urljoin, urlsplit, urlunsplit
import requests
import os
import json
from html import escape
import logging

from Patches.cssPatch import *
from Patches.urlPatch import *

cli = logging.getLogger("werkzeug")
cli.disabled = True

with open("config.json", "r") as file:
    config = json.load(file)

port = config["Port"]
proxyRoute = config["ProxyRoute"]
hostStatic = config["HostStatic"]
debugLog = config["DebugLogging"]

app = Flask(__name__)
app.logger.disabled = True
flask.cli.show_server_banner = lambda *args: None

logging.getLogger("werkzeug").disabled = True
app.logger.disabled = True

print("CatProxy")
print("Version: 0.2.0 (Nightly)")
print("https://github.com/Instel12/CatProxy/")
print(f"\nProxy starting at http://127.0.0.1:{port}/{proxyRoute}/")

@app.route(f"/{proxyRoute}/<path:url>")
def proxy(url):
    if url.startswith("cat://"):
        return send_from_directory("Internal", url[6:] + "/index.html")

    if debugLog:
        print(f"Requested \"{url}\"")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    query_string = request.query_string.decode("utf-8")
    if query_string:
        parsed = urlsplit(url)
        if parsed.query:
            url = urlunsplit(parsed._replace(query=f"{parsed.query}&{query_string}"))
        else:
            url = urlunsplit(parsed._replace(query=query_string))

    r = requests.get(url)
    content_type = r.headers.get("Content-Type", "")
    base = urljoin(url, "./")

    if "text/css" in content_type:
        css = rewriteCSS(r.text, url, proxyRoute)
        return Response(css, status=r.status_code, content_type=content_type)
    
    if "javascript" in content_type or "ecmascript" in content_type:
        js = patchURL(r.text, base, url)
        return Response(js, status=r.status_code, content_type=content_type)

    if "text/html" in content_type:
        HTMLconent = r.text
        scripts = ""

        if os.path.exists("Inject"):
            for file in os.listdir("Inject"):
                if file.endswith(".js"):
                    scripts += f"<script src='/Inject/{file}'></script>\n"

        injection = f"<script>window.CatProxyBase = '{escape(base)}';\nwindow.CatProxyOriginalUrl = '{escape(url)}';\nwindow.CatProxyRoute = '{proxyRoute}';</script>" + scripts

        if "<head>" in HTMLconent:
            HTMLconent = HTMLconent.replace("<head>", "<head>" + injection, 1)
        elif "</body>" in HTMLconent:
            HTMLconent = HTMLconent.replace("</body>", injection + "</body>", 1)
        else:
            HTMLconent += injection

        HTMLconent = patchURL(HTMLconent, base, url)
        HTMLconent = rewriteCSS(HTMLconent, url, proxyRoute)

        if debugLog:
            HTMLconent += """<div style="position: fixed; left: 0; top: 0; z-index: 9999999; background-color: black; color: red; font-family: sans-serif; padding: 0; margin: 0; font-size: 10px;">Developer mode enabled!<br>In other words, you currently lack privacy from who's hosting the proxy.</div>"""

        return Response(HTMLconent, status=r.status_code, content_type=content_type)

    return Response(r.content, status=r.status_code, content_type=content_type)


@app.route("/Inject/<path:filename>")
def injectStatic(filename):
    return send_from_directory("Inject", filename)
    
@app.route("/Internal/<path:filename>")
def internalStatic(filename):
    return send_from_directory("Internal", filename)

@app.route("/<path:filename>")
def staticFile(filename):
    if hostStatic:
        if debugLog:
            print(f'Requested "{filename}"')
        return send_from_directory("Static", filename)

@app.route("/")
def index():
    if hostStatic:
        if debugLog:
            print('Requested "index.html"')
        return send_from_directory("Static", "index.html")

@app.errorhandler(404)
def four04(error):
    return send_from_directory("Static", "404.html"), 404

app.run(port=port)