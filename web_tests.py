#!/usr/bin/python


import requests
# from web import *

response = requests.get("http://127.0.0.1:1234/")

assert response.status_code == 200
assert response.headers['connection'] == 'close'
assert response.headers['cache-control'] == 'nocache'
assert response.headers['content-type'] == 'text/plain'
assert response.headers['server'] == 'BaseHTTP/0.3 Python/2.7.3'
assert response.headers,get('date', None) != None

