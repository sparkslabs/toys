#!/usr/bin/python
#
# This may build on top of the BaseHTTPServer.py and implement a handler
# and it may also implement a sockets interface.
#
# HOWEVER, IT DOES NOT IMPLEMENT WEBSOCKETS
#
# In future though, it may do.
#
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
import time
from Queue import Queue

__version__ = 13.4

STATIC_MESSAGE= """\
<head>
<title>Standard Response</title>
</head>
<body>
<h1>Standard Response</h1>
<p>Some code %(code)d.
<p>Message: %(message)s.
<p>Some code explanation: %(code)s = %(explain)s.
</body>
"""

class WebResource( BaseHTTPRequestHandler ):
    def __init__(self, *argv, **argd):
        BaseHTTPRequestHandler.__init__(self, *argv, **argd)
        self.base = {}

    def version_string(self):
        """Return the server software version string."""
        return self.server_version + ' ' + self.sys_version + ' ' + "ToySock/"+str(__version__)


    def do_Headers(self):
        self.send_response(200)
        self.send_header("Cache-Control", "nocache")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):
        print "self.headers", self.headers
        print "type(self.headers)", type(self.headers)
        print "self.headers.__class__", self.headers.__class__
        print "dir(self.headers)", dir(self.headers)
        print "self.headers.keys()", self.headers.keys()
        print "_____________________"
        for header in self.headers:
          print header, self.headers.getheaders(header)
        print "dir(self)", dir(self)

        do_socks = False
        if "connection" in self.headers.keys():
          if self.headers.getheaders("connection") == ["Upgrade"]:
            do_socks = True

        if not do_socks:
          self.do_Headers()
          print self.path , self.path.split("/")
          parts =  self.path.split("/")
          if parts[0] != "":
              print "hmm"
              content = STATIC_MESSAGE % {"code": 101, "message" : "hello", "explain": "You have a malformed path: " + repr(self.path)}
          else:
              content = STATIC_MESSAGE % {"code": 101, "message" : "hello", "explain": self.path}
          self.wfile.write(content)
        else:
          print "DO SOCKS! DO SOCKS!"
          response = """\
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
""".replace("\n","\r\n")
          self.wfile.write(response)
          self.wfile.write("> \r\n")
# This next line fails at the moment...
#          line = self.rfile.readline()
#          self.wfile.write(line[::-1]+"\r\n")


import socket


class WebThread(threading.Thread):
  daemon = True
  readyQ = Queue()
  def run(self, server_listenip="127.0.0.1", port=1234):
    server_address = (server_listenip, port)

    protocol="HTTP/1.0"
    WebResource.protocol_version = protocol
    httpd = HTTPServer(server_address, WebResource)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    self.readyQ.put(True)
    httpd.serve_forever()

  def wait_ready(self):
    return self.readyQ.get()

wt = WebThread()
wt.start()

wt.wait_ready() # Blocking call, only one caller can call this.


# make and connect socket
import socket
import select
import errno

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.setblocking(0)
try:
  sock.connect(("127.0.0.1", 1234))
except socket.error, e:
  if e.errno == errno.EINPROGRESS: # Operation now in progress (expected exception)
    print "Connecting ..."
  else:
    print "Bollocks"
    raise

timeout = 1

# send request - example connection upgrade message, as per RFC 6455
# Request is currently effectively ignored
message = """\
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: http://example.com
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13

""".replace("\n","\r\n")

while len(message) > 0:
  readables, writeables, other = select.select([sock], [sock], [sock],timeout)
  if writeables != []:
      try:
        bytes_sent = sock.send(message)
        message = message[bytes_sent:] # Why have I never thought of that before?
      except socket.error, e:
        if not (e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK):
          raise

# get response
result = []
chunksize = 32
while True:
  readables, writeables, other = select.select([sock], [sock], [sock],timeout)
  print "Here?",readables, writeables, other 
  try:
    data = sock.recv(chunksize)
    if len(data)>0:
      result.append(data)
    else:
      break # EOF
  except socket.error, e:
    if not (e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK):
      raise

# print result
print "".join(result)

if 0:
  if other != []:
    print "oh bollocks"
  # If closing for some reason...

result = sock.shutdown(2)
sock.close()

