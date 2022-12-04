#!/usr/bin/python3.11

# ------------------------------------------  Import Decelerations -------------------------------------
import time
from IOLink import current_values  
from dotenv import dotenv_values

# ------------------------------------------ Variables -------------------------------------------------
conFigSettings = dotenv_values(".env") # load the settings from .env
deviceID = conFigSettings['deviceID'] # set the device ID
fCountDownSetPoint = conFigSettings['transmissionInterval'] # how often we will transupdate the DB/webapp / mqtt TX
xNewStep = false
iStep = 0
iStepOld = iStep
fStepInterval = 0.1
fCountDown = fCountDownSetPoint
# ------------------------------------------ Functions -------------------------------------------------

def getlevel(): # Get the level from Port 
    jdata = current_values()
    level = jdata["level"]
    if level == 8189:
        level = "FULL"
    return level


def gettemp(): # Get the current tempriture 
    jdata = current_values()
    temp = jdata["temp"]
    return temp


# ------------------------------------------ Main Control Sequence -------------------------------------------------
def mainsequence():
   
    while True:
         match iStep: # note match requires python version 3.1 or greater
            case 0:# init step
                print("Tank Check Starting " +str(iStep))
                print("deviceID = " +str(deviceID))
                iStep = iStep +1
            case 1:# Start MQTT service
                print("Reading Values" +str(iStep))
                print("Level = " +str(getlevel()))  
                print("Temp = " +str(gettemp()))  
                iStep = iStep +1              
            case 2:# Start Local API Service
                print("Start Local API Service" +str(iStep))
                iStep = iStep +1
            case 3:# Connect to Firebase
                print("Connect and update Firebase" +str(iStep))  
                iStep = iStep +1 
            case 10:# Run 
                if (xNewStep == True):
                     print("Wait " + str(fCountDownSetPoint) + " Seconds")  
                     fCountDown = fCountDownSetPoint # how often we will transupdate the DB/webapp / mqtt TX
                 
                fCountDown = (fCountDown - fStepInterval)
                if  (fCountDown<=0.0):
                    iStep = iStep +1 
            case 11:#Update firebase
                print("Connect and update Firebase" +str(iStep))  
                iStep = iStep -1 
        # while true 
         time.sleep(fStepInterval)
         if iStep == iStepOld:
            xNewStep = False
         else:
            xNewStep = True
         iStepOld = iStep


# ------------------------  Call main Sequence    -----------------------------------------
if __name__ == '__main__':
    mainsequence()
