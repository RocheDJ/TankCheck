#!/usr/bin/python3
import requests
import json

api_url = "http://10.15.1.106/iolinkmaster/port[2]/iolinkdevice/pdin/getdata"
response = requests.get(api_url)
iResponceCode = response.status_code
oJson = response.json()

iCID = oJson['cid'] # read the cid of the 
hexDataValue = oJson['data']['value'] # read the proecss data value from the system

print("Complete ,  Responce code = "+ str(iResponceCode) + " CID = " +  str(iCID) + " Value = " + str(hexDataValue))

iWord1 = int(hexDataValue,16) # only 14 bit word returned

iWord1 = iWord1/4  # only interested in the first 14 bits

fLevel = round(iWord1, 0) # 0 decimal place required

print("iWord1  = " + str(iWord1) )

if fLevel >= 8189  :
    print("Level mm = FULL")
else:
     print("Level mm = " + str(fLevel) )




