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

In order to store a value from toy
As a toy controller
I need the web service to accept a PUT request to a path

In order to retrieve a value from toy
As a toy controller
I need the web service to accept a GET request to a path

In order to retrieve timely information from a toy
As a toy controller
I need to webservice to accept web socket connection requests, and to update me when a resource changes

In order to control a toy in a timely fashion
As a toy controller
I need to webservice to accept web socket connection requests, to allow me to send it control messages.

In order to make the toy do something
As a toy controller
I need the toy's web service to accept a POST request to a path


