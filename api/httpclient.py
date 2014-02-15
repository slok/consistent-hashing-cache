import urllib.request
import urllib.parse


# Protocol URLS
protocol = {
    "get": "/get",
    "add": "/add",
    "add-node": "/add-node",
    "rm-node": "/rm-node",
    "stats": "/stats",
}


def do_request(url, data):
    if data:
        data = urllib.parse.urlencode(data)
        req = urllib.request.Request(url, data.encode("utf-8"))
    else:
        req = urllib.request.Request(url)

    f = urllib.request.urlopen(req)
    return f.read()

def get(host, key):

    url = "http://{0}{1}".format(host, protocol["get"])
    values = {'key': key}
    return str(do_request(url, values), "utf-8")

def add(host, key, data):
    url = "http://{0}{1}".format(host, protocol["add"])
    values = {'key': key, 'data': str(data)}
    return str(do_request(url, values), "utf-8")

def add_node(host, key):
    url = "http://{0}{1}".format(host, protocol["add-node"])
    values = {'node-key': key}
    return str(do_request(url, values), "utf-8")

def rm_node(host, key):
    url = "http://{0}{1}".format(host, protocol["rm-node"])
    values = {'node-key': key}
    return str(do_request(url, values), "utf-8")

def stats(host):
    url = "http://{0}{1}".format(host, protocol["stats"])
    return str(do_request(url, None), "utf-8")