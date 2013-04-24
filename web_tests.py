#!/usr/bin/python


verbose = False

import requests
from web import *
import time

def is_subdict(bigD,littleD):
  return set(littleD.items()).issubset(set(bigD.items()))

def blab(status):
  if verbose: print status

def smoke_test():
  response = requests.get("http://127.0.0.1:1234/")

  assert response.status_code == 200
  blab( "response status code : OK" )

  assert is_subdict( response.headers, {"connection": "close", "cache-control":"nocache", "content-type":"text/plain"})
  blab( "connection headers : OK" )

  assert "BaseHTTP/0.3 Python/2.7.3" in response.headers['server'] # Could be later version perhaps
  blab( "expected base server class : OK" )

  assert "ToyWebResource" in response.headers['server'] # Could be later version perhaps
  blab( "Is a toy web resource: OK" )

  s = response.headers['server']
  wt_version = float(s[s.rfind("/")+1:])
  assert wt_version >= 13.4
  blab( "Toy web resource able to cope with these tests (version> 13.4): OK" )

  assert response.headers,get('date', None) != None
  blab( "Date is not null: OK" )

  blab( "Date is fresh: (not checked)" )

wt = WebThread()
wt.start()

wt.wait_ready() # Blocking call, only one caller can call this.

smoke_test()


