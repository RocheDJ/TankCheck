#!/usr/bin/python3
import requests
import json

api_url = "http://10.15.1.106/iolinkmaster/port[1]/iolinkdevice/pdin/getdata"
response = requests.get(api_url)
iResponceCode = response.status_code
oJson = response.json()

iCID = oJson['cid'] # read the cid of the 
hexDataValue = oJson['data']['value'] # read the proecss data value from the system

print("Complete ,  Responce code = "+ str(iResponceCode) + " CID = " +  str(iCID) + " Value = " + str(hexDataValue))

iWord1 = int(hexDataValue,16)
iWord1 = int(iWord1/65536)  # only interested in the integer part
fDegC = iWord1 * 0.1

print("iWord1  = " + str(iWord1) )

print("Deg C  = " + str(fDegC) )


