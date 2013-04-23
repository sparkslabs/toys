#!/usr/bin/python

"""
$ clear ;echo -ne "PUT /hello/world HTTP/1.0\nContent-Length: 12\n\nHello World\n"|netcat 127.0.0.1 1234 -
"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
import time

def Print(*argv, **argd):
    print argv, argd

class Resource(object):
    def __init__(self):
        self.value = None
        self.function = Print
        #
    def get(self):
        print "GET"
        return self.value
        #    
    def set(self, value):
        print "SET"
        self.value = value
        #
    def __call__(self, *argv, **argd):
        print "CALL"
        self.function(*argv, **argd)

DEFAULT_ERROR_MESSAGE = """\
<head>
<title>Error response</title>
</head>
<body>
<h1>Error response</h1>
<p>Error code %(code)d.
<p>Message: %(message)s.
<p>Error code explanation: %(code)s = %(explain)s.
</body>
"""


class WebResource( BaseHTTPRequestHandler ):
    def __init__(self, *argv, **argd):
        BaseHTTPRequestHandler.__init__(self, *argv, **argd)
        self.base = {}

    def do_Headers(self):
        self.send_response(200)
        self.send_header("Cache-Control", "nocache")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):
        self.do_Headers()
        print self.path , self.path.split("/")
        parts =  self.path.split("/")
        if parts[0] != "":
            print "hmm"
            content = DEFAULT_ERROR_MESSAGE % {"code": 101, "message" : "hello", "explain": "You have a malformed path: " + repr(self.path)}
        else:
            content = DEFAULT_ERROR_MESSAGE % {"code": 101, "message" : "hello", "explain": self.path}
        self.wfile.write(content)

    def do_PUT(self):
        self.do_Headers()
        print "", self.headers, self.headers.get("Content-Length",-1)
        if self.headers.get("Content-Length",-1) >0:
            x = self.rfile.read(int(self.headers.get("Content-Length")))
            message = x
        else:
            message = "Flibberty"

        content = DEFAULT_ERROR_MESSAGE % {"code": 101, "message" : message, "explain": self.path}

        self.wfile.write(content)

    def do_POST(self):
        self.do_Headers()
        print "", self.headers, self.headers.get("Content-Length",-1)
        if self.headers.get("Content-Length",-1) >0:
            x = self.rfile.read(int(self.headers.get("Content-Length")))
            message = x
        else:
            message = "Flibberty"

        content = DEFAULT_ERROR_MESSAGE % {"code": 101, "message" : message, "explain": self.path}

        self.wfile.write(content)

class WebThread(threading.Thread):
  daemon = True

  protocol="HTTP/1.0"
  port = 1234
  server_listenip = ''

  def run(self):
    server_address = (self.server_listenip, self.port)

    WebResource.protocol_version = self.protocol
    httpd = HTTPServer(server_address, WebResource)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()


if __name__ == "__main__":
  r = Resource()
  r.set(5)
  r.get()
  r("hello", "world")

  wt = WebThread()
  wt.start()

  while True:
    time.sleep(0.1)
