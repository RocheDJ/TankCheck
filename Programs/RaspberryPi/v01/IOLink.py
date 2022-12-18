#!/usr/bin/python3
#------------------------------------------------------------------------------------------------
# By: David Roche
# Date: December 2022
# Description : IO link interface to IFM Al1350
#------------------------------------------------------------------------------------------------
#--------------------- Linked Libraries -----------------
import requests
import json
from dotenv import dotenv_values

# load config settings
conFigSettings = dotenv_values(".env")
api_url_Port1 = conFigSettings['Port1']
api_url_Port2 = conFigSettings['Port2']

def current_values():
    #read the temp values
    try:
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
    except:
        temperature=0.00 # invalid data value
        print("An exception occurred")
        
    try:
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
    except:
        fLevel=0.00 # invalid data value
        print("An exception occurred")  
    #return the data
    msg = {"temp":temperature,"level":fLevel}
    return msg
