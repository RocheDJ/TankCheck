#!/usr/bin/python3.11
# -------------------------------------------- blynk decelerations 
#define BLYNK_TEMPLATE_ID "TMPL7YZ5aLRv"
#define BLYNK_DEVICE_NAME "Silo 1001" 
#define BLYNK_AUTH_TOKEN "zNxJ3hkSxs2eal-XM4bwSwujxYxfMpcj
# ------------------------------------------  Import Decelerations -------------------------------------
import storeDataDB
import datetime
import time
from time import sleep
import webapi
from IOLink import current_values  
from dotenv import dotenv_values
import RPi.GPIO as GPIO # use the gpio bus on the Rpi 
import BlynkLib
from multiprocessing import Process
# ------------------------------------------ Variables -------------------------------------------------
conFigSettings = dotenv_values(".env") # load the settings from .env
siloID = conFigSettings['siloID'] # set the device ID
BLYNK_AUTH = conFigSettings['blynk_auth'] 

# ------------------------------------------ Functions -------------------------------------------------
# get config data for silo
def updateSilo(sSiloID):
    sProduct = conFigSettings['product'] 
    iMax_mm = conFigSettings['max_mm'] 
    iMin_mm = conFigSettings['min_mm'] 
    iMax_ltr = conFigSettings['max_ltr'] 
    iMin_ltr = conFigSettings['min_ltr'] 
    
    storeDataDB.push_db_silo(sSiloID,iMax_mm,iMin_mm,
                            iMax_ltr,iMin_ltr,
                            sProduct)

# get values and send to firebase
def updateReading(sSiloID,iReadcount):
    jdata = current_values()
    celcius = jdata["temp"]
    level = float(jdata["level"])
    iMax_mm = float(conFigSettings['max_mm']) 
    if (level >= 8189.0):
        level =iMax_mm
    currentTime = datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
    # Converting DateTime into epoch time in milliseconds using Python
    eDateTime = datetime.datetime.now().timestamp() *1000 # see reference https://www.javatpoint.com/python-epoch-to-datetime

    xActuater =  GPIO.input(10)
    print("xActuater = " +str(xActuater))
    storeDataDB.push_db_silo_reading(sSiloID,iReadcount,celcius, level,xActuater,currentTime,eDateTime)
    publish_Blynk(level,celcius)
     
# start the web interface to run as a seperate process     
def startWEBAPI(fDelay,xDebugMode):
    webapi.runWebAPI(fDelay,xDebugMode)

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

def publish_Blynk(iLevel,iTemp):
    blynk.virtual_write(1, iTemp) 
    blynk.virtual_write(2,round(get_uptime(),0))
    blynk.virtual_write(3, iLevel)

# ------------------------------------------ BLYNK                  -------------------------------------------------
# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH) #auth key

# register handler for virtual pin V0 write event
@blynk.on("V0")

def v3_write_handler(value):
    buttonValue=value[0]    
    if buttonValue=="1":
        GPIO.output(10, True)
    else:
        GPIO.output(10, False)
# ------------------------------------------ Main Control Sequence -------------------------------------------------
def mainsequence():
    fCountDownSetPoint = float(conFigSettings['transmissionInterval']) # how often we will transupdate the DB/webapp / mqtt TX
    xNewStep = 0
    iStep = 0
    iStepOld = iStep
    fStepInterval = 0.1
    fCountDown = fCountDownSetPoint
    xWebDebug=conFigSettings['localWebAPIDebug']
    iReadcount = 0 # store last 10 readings in a buffor
    iTemp =0
    iLevel =0
    # create a process
    process = Process(target=startWEBAPI,args=(1.0, xWebDebug))
    try:
      while True:
            # ----------------------   Step 0  ---------------------
            if iStep == 0:# init step
                print("Step: " + str(iStep) + " Tank Check Starting " )
                print("Silo ID = " +str(siloID))
                iStep = iStep +1
            # ----------------------   Step 1  ---------------------
            elif iStep == 1:# Push Data To Blynk
                print("Step: " + str(iStep) + " Start xxx ")
                iStep = iStep +1 
            # ----------------------   Step 2  ---------------------             
            elif iStep ==  2:# Start Local API Service
                print("Step: " + str(iStep) + " Start Local API Service ")
                # run the process
                process.start()
                iStep = iStep +1
            # ----------------------   Step 3  ---------------------
            elif iStep == 3:# Connect to Firebase update settings
                print("Step: " + str(iStep) + " Push Config Data For Silo ") 
                updateSilo(siloID)
                iStep = 10 
            # ----------------------   Step 10  ---------------------
            elif iStep ==  10:# Run 
                if (xNewStep == 1):
                     print("Step: " + str(iStep) + " Wait " + str(fCountDownSetPoint) + " Seconds Please :-)")  
                     fCountDown = fCountDownSetPoint 
                
                fCountDown = (fCountDown - fStepInterval)
              
                if (fCountDown<0.0):
                    iStep = iStep +1
            # ----------------------   Step 11  --------------------- 
            elif iStep ==  11:#Update firebase
                if (xNewStep == 1):
                    print("Step: " + str(iStep) + " Updating Reading")  
                    updateReading(siloID,iReadcount)
                    iReadcount = iReadcount +1 #incrament count
                    if iReadcount > 9 :
                        iReadcount =0 # count clamped to 10 records
                iStep = iStep + 1 
            # ----------------------   Step 12  --------------------- 
            elif iStep ==  12:#Update firebase
                if (xNewStep == 1):
                    print("Step: " + str(iStep) + " Repeat ")  
                iStep = iStep + 1 
            # ----------------------   Step 13  --------------------- 
            elif iStep ==  13:#read Agittator
                if (xNewStep == 1):
                    xSPOn = storeDataDB.read_agitator(siloID)
                    if xSPOn == True:
                       GPIO.output(10, True)
                       #print("Agitator ON")
                    else:
                        GPIO.output(10, False)
                        #print("Agitator Off")  
                    print("Step: " + str(iStep) + " Repeat ")  
                    
                iStep = 10 
            # ----------------------  Catch All  ---------------------      
            else: 
                iStep =0
            time.sleep(fStepInterval)
            if iStep == iStepOld:
                xNewStep = 0
            # ----------------------   Step XX  ---------------------
            else:
                xNewStep = 1
                iStepOld = iStep

            
            blynk.run()
            #sleep(.5)

    except KeyboardInterrupt:
        print("Good Bye")  
        GPIO.cleanup()  
# ------------------------  Call main Sequence    -----------------------------------------
if __name__ == '__main__':
    mainsequence()
