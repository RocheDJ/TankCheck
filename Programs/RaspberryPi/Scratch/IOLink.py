#!/usr/bin/python3
import requests
import json

api_url_Port1 = "http://10.15.1.106/iolinkmaster/port[1]/iolinkdevice/pdin/getdata"
api_url_Port2 = "http://10.15.1.106/iolinkmaster/port[2]/iolinkdevice/pdin/getdata"
deviceID = "iolinkmaster1"


def current_values():
    #read the temp values
    response = requests.get(api_url_Port1) # send request to IOlink master
    iResponceCode = response.status_code # read the responce code
    if iResponceCode == 200:
        oJson = response.json() # read the json responce string
        hexDataValue = oJson['data']['value'] # read the proecss data value from the system
        iWord1 = int(hexDataValue,16)
        iWord1 = int(iWord1/65536)  # only interested in the integer part
        fDegC = iWord1 * 0.1
        temperature=round(fDegC,2)
    else:
        temperature=0.00 # invalid data value
       
   # read the level data
    response = requests.get(api_url_Port2) # send request to IOlink master
    iResponceCode = response.status_code # read the responce code
    if iResponceCode == 200:
        oJson = response.json() # read the json responce string
        hexDataValue = oJson['data']['value'] # read the proecss data value from the system
        iWord1 = int(hexDataValue,16) # only 14 bit word returned
        iWord1 = iWord1/4  # only interested in the first 14 bits
        fLevel = round(iWord1, 0) # 0 decimal place required
    else:
        fLevel=0.00 # invalid data value
    #return the data
    msg = {"deviceID": deviceID,"temp":temperature,"level":fLevel}
    return msg
