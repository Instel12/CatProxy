from flask import Flask, Response, request, send_from_directory
import flask.cli
from urllib.parse import urljoin, urlsplit, urlunsplit
import requests
import os
import json
from cssRewrite import *
from html import escape
import logging

cli = logging.getLogger("werkzeug")
cli.disabled = True

with open("config.json", "r") as file:
    config = json.load(file)

port = config["Port"]
proxyRoute = config["ProxyRoute"]
hostStatic = config["HostStatic"]

app = Flask(__name__)
app.logger.disabled = True
flask.cli.show_server_banner = lambda *args: None

logging.getLogger("werkzeug").disabled = True
app.logger.disabled = True

print("CatProxy")
print("Version: 0.1.2")
print("https://github.com/Instel12/CatProxy/")
print(f"\nProxy starting at http://127.0.0.1:{port}/{proxyRoute}/")

@app.route(f"/{proxyRoute}/<path:url>")
def proxy(url):
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

    if "text/css" in content_type:
        css = rewriteCSS(r.text, url, proxyRoute)
        return Response(css, status=r.status_code, content_type=content_type)

    if "text/html" in content_type:
        HTMLconent = r.text
        scripts = ""

        if os.path.exists("Inject"):
            for file in os.listdir("Inject"):
                if file.endswith(".js"):
                    scripts += f"<script src='/Inject/{file}'></script>\n"

        base = urljoin(url, "./")

        injection = (
            f"<script>window.CatProxyBase = '{escape(base)}';\n"
            f"window.CatProxyOriginalUrl = '{escape(url)}';\n"
            f"window.CatProxyRoute = '{proxyRoute}';</script>" + scripts
        )

        if "<head>" in HTMLconent:
            HTMLconent = HTMLconent.replace("<head>", "<head>" + injection, 1)
        elif "</body>" in HTMLconent:
            HTMLconent = HTMLconent.replace("</body>", injection + "</body>", 1)
        else:
            HTMLconent += injection

        return Response(HTMLconent, status=r.status_code, content_type=content_type)

    return Response(r.content, status=r.status_code, content_type=content_type)


@app.route("/Inject/<path:filename>")
def injectStatic(filename):
    return send_from_directory("Inject", filename)

@app.route("/<path:filename>")
def staticFile(filename):
    if hostStatic:
        print(f'Requested "{filename}"')
        return send_from_directory("Static", filename)

@app.route("/")
def index():
    if hostStatic:
        print('Requested "index.html"')
        return send_from_directory("Static", "index.html")

@app.errorhandler(404)
def four04(error):
    return send_from_directory("Static", "404.html"), 404

app.run(port=port)