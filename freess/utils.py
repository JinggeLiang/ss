
import base64
import dns.resolver
import re
import requests
import urllib.parse as urlparse


def bs64_decode(string, encoding="utf-8"):
    string += "=" * ((4 - len(string) % 4) % 4)
    b = bytes(string, encoding)
    d = base64.decodebytes(b)
    return d.decode(encoding)


def bs64_encode(string, encoding="utf-8"):
    b = bytes(string, encoding)
    d = base64.encodebytes(b)
    return d.decode(encoding).replace("\n", "")


def get_unicode(string):
    return string.encode("unicode_escape").decode("ascii")


def url_decode(string):
    return urlparse.unquote(string, "utf-8")


def url_encode(string):
    return urlparse.quote(string, "utf-8")


def get_ip_address(domain):
    try:
        r = dns.resolver.resolve(domain, 'A')
        return "".join([str(i) for a in r.response.answer for i in a.items if i.rdtype == 1][0])
    except:
        return "127.0.0.1"


def get_server_location(server):
    ip_rex = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    rex = re.compile(r"[0-9a-zA-Z_.]+")
    if ip_rex.search(server):
        ip = server
    elif rex.match(server):
        ip = get_ip_address(server)
    else:
        return server
    url = "https://api.ip.sb/geoip/" + ip
    response = requests.get(url)
    if response.status_code == 200:
        if response.json()["isp"] == "Cloudflare":
            return response.json()["isp"] + " - " + response.json()["country_code"]
        return response.json()["country"] + " - " + server


def get_github_file_sha(url):
    url = url
    response = requests.get(url).json()
    if response.get("sha"):
        return response["sha"]
    return ""


def update_github_file(token, url, string):
    url = url
    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": "token " + token,
    }
    data = {
        "content": bs64_encode(string),
        "message": "Update",
        "sha": get_github_file_sha(url)
    }
    response = requests.put(url=url, headers=headers, json=data).json()
    if response.get("content"):
        print("file updated.")
