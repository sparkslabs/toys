#!/usr/bin/python

class Value(object):
    def __init__(self, value):
         self.value = value
         self.store = Store()

class Store(object):
    def __init__(self):
        self.store = {}

    def getRepresentation(self, request):
        print "getRepresentation", request, None
        if request == "/":
            return self.store.keys()
        if request[0] != "/":
            return "FAIL"
            
        bits = request[1:].split("/")
        hint = bits[0]
        if len(bits) == 1: # Base case
            result = {
                "id": request, # Intriguing...
                "value" : self.store[hint].value
            }
            return repr(result)
        return "not yet supported"

    def storeRepresentation(self, request, value):
        print "storeRepresentation", request, value
        if request == "/":
           return "FAIL"

        if request[0] != "/":
           return "FAIL"
           
        bits = request[1:].split("/")
        hint = bits[0]
        if len(bits) == 1: # Base case
            try:
                value = self.store[hint].value
            except KeyError:
                self.store[hint] = Value(value)
            return self.store[hint]
        
        sub_store = self.store[hint].store
        print sub_store
        return "not yet supported"

S = Store()
print S.getRepresentation("/")
print
# print S.storeRepresentation("/", "hello")
# print
# print S.storeRepresentation("hello/", "hello")
# print
print S.storeRepresentation("/hello", "hello")
print
print S.getRepresentation("/hello")
print
print S.storeRepresentation("/hello/greeting", "hello")
print

