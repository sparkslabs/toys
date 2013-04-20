#!/usr/bin/python

import weakref
import json
import inspect
import gc

def html(thing):
    return thing.__html__()

def JSON(thing):
    return thing.__json__()

def asdict(thing):
    return thing.__asdict__()

class AutoResource(object):
    __namespace__ = None
    def __init__(self, argd, sig):
        # print "Called?",argd, sig
        self.__dict__.update(argd)
        args=inspect.getargspec(sig)[0][1:]
        self.__args = args
        self.__all__.add(weakref.ref(self))
    def __asdict__(self):
        result = {
            "__class__" : self.__class__.__name__,
            "__id__" : id(self),
        }
        for key in self.__args:
          result[key] = self.__dict__[key]
        return result
    @classmethod
    def __get_all__(cls):
        print "gc.collect()"
        gc.collect()
        return [x() for x in cls.__all__ if x() != None ]
    def __repr__(self):
        try:
          result = self.__class__.__name__ + "("
          items = []
          for key in self.__args:
            items.append(key + "=" + repr(self.__dict__[key]))
          result += ", ".join(items) + ")"
          return result
        except: # In case called before __init__
          return object.__repr__(self)
    def __str__(self):
        try:
          result = repr(self) + "_id=" + str(id(self))
          return result
        except: # In case called before __init__
          return object.__str__(self)
    def __json__(self):
        return json.dumps(self.__asdict__())
    def __html__(self):
        result = self.__asdict__()
        if self.__namespace__:
          result["__class__"] = self.__namespace__ + "_" + result["__class__"]
        for key in self.__args:
          result[key+"_key"] = key
        result_template =  []
        result_template.append('''<div class="%(__class__)s" id="obj%(__id__)s">''')
        result_template.append('''  <dl>''')
        for key in self.__args:
            result_template.append('    <dt class="'+key+'_key">%(' + key + '_key)s</dt>' + 
                                   '<dd class="'+key+'">%(' + key + ')s</dd>')
        result_template.append('''  </dl>''')
        result_template.append('''</div>''')
        return "\n".join(result_template) % result
    def __del__(self):
        print self, self.__all__
        for i in self.__all__:
            if i() == self:
                print "Deleting me!", self
        try:
            super(AutoResource,self).__del__(self)
        except AttributeError:
            pass

def autoinit(g):
  def f(self,*argv, **argd):
      print self, type(self),argv, argd
      args=inspect.getargspec(g)[0][1:]
      super(type(self),self).__init__(dict(zip(args,argv)), g)
      return g(self,*argv,**argd)
  return f

class Person(AutoResource):
    __namespace__ = None
    __all__ = set()
    @autoinit
    def __init__(self, forename, surname, address):
        pass

class Book(AutoResource):
    __namespace__ = None
    __all__ = set()
    @autoinit
    def __init__(self, author, title, synopsis):
        pass

person = Person("michael", "sparks", "mcuk")
otherperson = Person("michael", "smith", "mcuk")
anotherperson = Person("Matt", "smith", "cardiff")

Person.__get_all__()

gc.get_referrers(x) for x in gc.get_objects() if  type(x) == Person]

# if __name__=="__main__":
if 1:
    person = Person("michael", "sparks", "mcuk")
    lotr = Book("Tolkien", "LOTR", "Chuck a stone in a volcano")
    print str(person)
    print str(lotr)
    print asdict(person)
    print repr(JSON(person))
    print html(person)
    print asdict(lotr)
    print repr(JSON(lotr))
    print html(lotr)
    #print str(person)
    #print repr(asdict(person))
    #person.__namespace__ = "main"
    #print html(person)

person = Person("michael", "sparks", "mcuk")
otherperson = Person("michael", "smith", "mcuk")
anotherperson = Person("Matt", "smith", "cardiff")
