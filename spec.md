Role - Toy:
  Is a device
  Presents a web interface
  Is introspectable
  Provides access to resources providing information about the toy
  Performs tasks when POST requests are made to behaviour resources
  Behaviours provide a functional bridge to a device's actuators, and possible to sensors
  Sensors on the device may be exposed directly as information resources.
  Change to a resource may cause a change in behaviour, but not initiate a behaviour - for example a target speed may be set for a moving vehicle.
  What is a behaviour resource and what is a resource is up to the device.
  Initial devices are relatively dumb devices

Role Toy Controller:
  Is a device
  May be operated directly
  Communicates with one or more Toys in the local vicinity using a Web API

Story: Later on down the line:

  In order to retrieve timely information from a Toy
  As a Toy Controller
  I need to webservice to accept web socket connection requests, and to update me when a resource changes

  In order to control a toy in a timely fashion
  As a Toy Controller
  I need to webservice to accept web socket connection requests, to allow me to send it control messages.

Thoughts:
  When a toy recieves a message (get, put, post) for a resource it doesn't publish, it should throw back a web exception

  A web exception needs defining
    A web exception is an application concept sitting on top of an HTTP concept
    It is likely to a be a 400 error for undefined values
    For values relating to misuse of a behaviour a 500 series reponse is likely to ve appropriate

  A web value needs defining

Story: Basic protocol interaction
  In order to set a value
  As a WebAPIUser
  I need to PUT a WebValue to an URI

  In order to retrieve a value
  As a WebAPIUser
  I need to GET a WebValue from an URI

  In order to trigger functionality in a device
  As a WebAPIUser
  I need to POST WebParameters to an URI

  In order to denote exceptional behaviour in response to invalid WebParameters or invalid system state
  As a WebAPIProvider
  I need to respond with a WebException
  
  In order to understand what has gone wrong with a particular request
  As a WebAPIUser
  I need to WebAPIProvider to include details regarding what went wrong, where it went wrong, when it went wrong, why it went wrong, "who" is responsible for the fault, and if possible how to rectify the problem - in short errors need to be as verbose as practical

Story: Functional Object Mapping
  In order to group functionality in a Toy
  As a WebAPIProvider
  I need to be able to indicate that a resource is a object with behaviours

  In order to identify a behaviour in a Toy
  As a as WebAPIProvider
  I need to be able to indicate in its GET WebValue that the WebValue describes a behaviour

  In order identify the object a behaviour refers to in a Toy
  As a WebAPIProvider
  I need to be able to map /functionalobject/behaviour - back to /functionalobject

  In order to simplify the WebAPI
  As a WebAPIProvider
  I need to be able to treat attributes, behaviours and functional objects in a common way

  Scenarios:
     Given /robot refers to a functional object
     If a WebAPIUser makes a GET request to the URI /robot/arm
     Then the WebAPIProvider should return a WebValue describing the /robot/arm attribute, which is in this case of type functional object, and itself contains attributes and behaviours

     Given /robot/arm is a functional object containing 2 resources - "position" and "moveto"
     If a WebAPIUser makes a GET request to the URI /robot/arm/
     Then the WebAPI should respond with a collection describing the names contained within the collection, and optional further type information. (undecided)

     Given /robot/arm is a functional object containing 2 resources - "position" and "moveto"
     If a WebAPIUser makes a GET request to the URI /robot/arm/position
     Then the WebAPIProvider should request (GET) the "position" attribute from the /robot/arm functional object and return the WebValue to the WebAPIUser
     The WebValue may additionally include information noting the position is 

     Given /robot/arm is a functional object containing 2 resources - "position" and "moveto"
     If a WebAPIUser makes a GET request to the URI /robot/arm/moveto
     Then the WebAPIProvider should request (GET) the "moveto" attribute from the /robot/arm functional object and return the WebValue to the WebAPIUser
     Also the WebValue in this case describes a behaviour - behaviours may take time to complete.

     Given /robot/arm is a functional object containing 2 resources - "position" and "moveto"
     If a WebAPIUser makes a PUT request to the URI/robot/arm/position to change the position to 10
     Then the WebAPIProvider should respond with a WebException, because the position attribute is a consequence of the moveto behaviour

Story: Toy history is repeatable
  In order to debug events, in a system
  As a WebAPIUser
  I need to WebAPIProvider to provder an ongoing history of WebValues, WebExceptions, and a log of incoming events

  Comment: This is akin to an access log and error log, with the further detail of logging what is sent back out in both cases.
    There are security implications regarding this as well, but there are potential automation benefits
    This is similar to every device providing an RSS feed regarding it's activity
    
    It is likely that some devices could not provide this.

Story: Getting things started:

  In order to store a value from Toy
  As a Toy Controller
  I need the web service to accept a PUT request to a path

  In order to retrieve a value from Toy
  As a Toy Controller
  I need the web service to accept a GET request to a path

  In order to make the Toy do something
  As a Toy Controller
  I need the Toy's web service to accept a POST request to a path

