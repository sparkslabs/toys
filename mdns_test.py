#!/usr/bin/python

#
# Testing using pybonjour, version 1.1.1
#
# Basic smoke test/play test, so see what the library is like.
# Not indicitive of what the final functionality might be, let alone how it'd be implemented
# 

import select
import sys
import pybonjour

class toyService(object):
    def __init__(self, name="toy_bot", regtype="_iotoy._tcp", port = 8080):
        self.name = name
        self.regtype = regtype
        self.port = port
        self.sdRef = None

    def callback(self, sdRef, flags, errorCode, name, regtype, domain):
        print sdRef, flags, errorCode, name, regtype, domain
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print 'Registered service:'
            print '  name    =', name
            print '  regtype =', regtype
            print '  domain  =', domain

    def main(self):
        self.sdRef = sdRef = pybonjour.DNSServiceRegister(name = self.name, regtype = self.regtype, port = self.port, callBack = self.callback)
        try:
            try:
                while True:
                    ready = select.select([sdRef], [], [])
                    if sdRef in ready[0]:
                        pybonjour.DNSServiceProcessResult(self.sdRef)
            except KeyboardInterrupt:
                pass
        finally:
            sdRef.close()

    def webFront(self):
        # stub - this is one possible location for the server to be defined/configured. Perhaps.
        pass

toyservice = myService()

toyservice.main()

