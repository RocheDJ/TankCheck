# SETU HDip Computer Science

HDip Computer Systems and Networks Assignment IOT

---

## Originator

- David Roche

## Student ID  

- 93521243

---

### **Project Background**

This is an industrial project based in the dairy sector, specifically in the area of milk collection and haulage.
The proposed system will try to address three specific problems.

- 1) When a haulier goes to a farm to collect milk, ideally the milk should be agitated to make sure it can be correctly metered.
This means that the driver has to turn on an agitator inside the bulk tank then wait for a time period until the milk has been correctly agitated.
This leads to lost time and lost revenue on farm for the haulier.

- 2) Off peak collections can be erratic with yields fluctuating leading to collection amounts varying considerably, this in turn leading to less or more than expected amounts to be collected. This can cause issues with route planning and scheduling.

- 3) Milk too hot to collect, if the farm vat chiller is malfunctioning or milking has just taken place then the raw milk can be too hot to collect, leading to rescheduled pickup or milk being collected too hot and reducing to overall temperature  and therefore quality of the collected product already in the collection tanker

---

### **Project Description**

This project will aim to develop a prototype solution to;

- Monitor the level and temperature in the tank/silo using existing food grade approved industrial sensors.

- Send the live data into a cloud hosted DB which will have simple Web UI to display those values for haulier and farm manager.

- Allow the driver to activate the tank agitator when they leave the depot or previous farm.

---

### **Tools, Technologies and Equipment**

- The sensors and actuators will connect to an [IOLink](https://io-link.com/en/Technology/what_is_IO-Link.php?thisID=76) Master, with an ethernet interface.
The IO link master has a built in API to allow for data access.

- The prototype solution will use a **Raspberry Pi** to

  - Communicate to the IO Link master over TCP reading information using it's API. 

  - Communicate using MQTT to a cloud based service to publish Level, Temperature and Actuator values .

  - Communicate to a cloud based service to allow the haulier /driver to activate the agitator remotely if required.

  - Host a local Web API to allow local access on the network to current Level, Temperature and Actuator values.

- IOLink Mater will be an IFM [AL1350](https://www.ifm.com/ie/en/product/AL1350).

- The Raspberry Pi and the IOLinkMaster will be connected to a Teltonkia [RUT955 Industrial Cellular Router](https://teltonika-networks.com/product/rut955/) which wil provide internet connectivity.

- The Raspberry Pi development is written in Python.

---

### **Github Repo**

A repository for the Assignment is here project is here

- [GitHubRepo](https://github.com/RocheDJ/TankCheck)

---

### **Web App**

A demo web app has been developed in Node JS and is deployed here

- [TankCheck Web App](https://djr-silocheck.glitch.me/)

---



### **Video**

- [Assessment Video]()

---
### **External References**

- [HTML and CSS in FLASK](https://thinkinfi.com/flask-adding-html-and-css/)

- [Firebase reading and writing data](https://firebase.google.com/docs/database/web/read-and-write#read_data_once)

- [Python API interrogation](https://realpython.com/api-integration-in-python/)

- [Running Multi Processes in Python](https://superfastpython.com/run-function-in-new-process/)

- [Firebase 101 NoSWL DB management](https://devblogs.microsoft.com/premier-developer/firebase-101-nosql-database-management/)

- [W3 schools Python reference](https://www.w3schools.com/python/python_reference.asp)