#!/usr/bin/python3
#------------------------------------------------------------------------------------------------
# By: David Roche
# Date: December 2022
# Description : Main Raspberry Pi Application 
#------------------------------------------------------------------------------------------------

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
iIOChannel =26
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

    xActuater =  GPIO.input(iIOChannel)
    print("xActuater = " +str(xActuater))
    storeDataDB.push_db_silo_reading(sSiloID,iReadcount,celcius, level,xActuater,currentTime,eDateTime)
    publish_Blynk(level,celcius)
     
# start the web interface to run as a seperate process     
def startWEBAPI(fDelay,xDebugMode):
    webapi.runWebAPI(fDelay,xDebugMode)

# get the ptime of the Pi
def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

# publish data to blynk service
def publish_Blynk(iLevel,iTemp):
    blynk.virtual_write(1, iTemp) 
    blynk.virtual_write(2,round(get_uptime(),0))
    blynk.virtual_write(3, iLevel)
    if agitator_state():
        blynk.virtual_write(4, 1)
    else:
        blynk.virtual_write(4, 0)

def agitator_control(xSwitch):
    GPIO.output(iIOChannel, xSwitch)
    if agitator_state():
        blynk.virtual_write(4, 1)
    else:
        blynk.virtual_write(4, 0)

def agitator_state():
    if (GPIO.input(iIOChannel) == 1) :
        xOn = True
    else:
        xOn = False   
    return xOn

def initRaspberryPiGPIO(iChannelNo):
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # naming convention is to be used.
        GPIO.setup(iChannelNo, GPIO.OUT)
        GPIO.output(iChannelNo, False)
    except:
        print("An exception occurred Configuring GPIO")

# ------------------------------------------ BLYNK                  -------------------------------------------------
 # initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH) #auth key
# register handler for virtual pin V0 write event
@blynk.on("V0")

def v3_write_handler(value):
    buttonValue=value[0]
    print("Agitator Blynk Control "  + str(buttonValue))      
    if buttonValue=="1":
        agitator_control(True)
    else:
        agitator_control(False)

# ------------------------------------------ Main Control Sequence -------------------------------------------------
def mainsequence():
    fUpdateSetPoint = float(conFigSettings['transmissionInterval']) # how often we will transmit level to firebase
    fPolingSetPoint = float(conFigSettings['poolingInterval']) # how pool firebase for agitator update
    fOnTimeSetPoint = float(conFigSettings['agitatorOntime']) # turn on for x seconds when triggered
    xOldDBTrigger = False
    xOldAPITrigger = False
    xNewStep = 0
    iStep = 0
    iStepOld = iStep
    fStepInterval = 0.1
    fCountDown = fUpdateSetPoint
    fPoolingCountDown = fPolingSetPoint
    fAgitatorCountDown= fOnTimeSetPoint
    if conFigSettings['localWebAPIDebug'] == 'True':
        xWebDebug=True
    else:
        xWebDebug=False

    iReadcount = 0 # store last 10 readings in a buffor
    iTemp =0
    iLevel =0
    # create a process fro the Web API
    procWebAPI = Process(target=startWEBAPI,args=(1.0, xWebDebug))
    try:
      while True:
            # ----------------------   Step 0  ---------------------
            if iStep == 0:# init step
                print("Step: " + str(iStep) + " Tank Check Starting " )
                print("Silo ID = " +str(siloID))
                print("MaxOn time = " +str(fOnTimeSetPoint) + "sec")
                initRaspberryPiGPIO(iIOChannel)
                iStep = iStep +1
            # ----------------------   Step 1  ---------------------
            elif iStep == 1:# 
                print("Step: " + str(iStep) + " Start Blynk ")
                iStep = iStep +1 
            # ----------------------   Step 2  ---------------------             
            elif iStep ==  2:# Start Local API Service
                print("Step: " + str(iStep) + " Start Local API Service ")
                # run the process
                procWebAPI.start()
                iStep = iStep +1
            # ----------------------   Step 3  ---------------------
            elif iStep == 3:# Connect to Firebase update settings
                print("Step: " + str(iStep) + " Push Config Data For Silo ") 
                updateSilo(siloID)
                iStep = 10 
            # ----------------------   Step 10  ---------------------
            elif iStep ==  10:# Run 
                if (xNewStep == 1):
                     print("Step: " + str(iStep) + " Wait " + str(fUpdateSetPoint) + " Seconds Please :-)")  
                     fCountDown = fUpdateSetPoint 
                # check pooling for agitator state on firebase
                fPoolingCountDown = (fPoolingCountDown - fStepInterval)
                if (fPoolingCountDown<=0.0):
                    fPoolingCountDown = fPolingSetPoint
                    xSPOn = storeDataDB.read_agitator(siloID)
                    if not (xSPOn == xOldDBTrigger): # only trigger change on rising of falling edge
                        if xSPOn == True:
                            agitator_control(True)
                        else:
                            agitator_control(False) 
                    xOldDBTrigger = xSPOn
                # check timeout for data update      
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
                        iReadcount = 0 # count clamped to 10 records
                iStep = iStep + 1 
            # ----------------------   Step 12  --------------------- 
            elif iStep ==  12:#Retrun to run Step
                if (xNewStep == 1):
                    print("Step: " + str(iStep) + " Repeat ")  
                iStep = 10 
            # ----------------------  Catch All  ---------------------      
            else: 
                iStep =0

            # ----------------------End of loop tasks------------------   
          

            if iStep == iStepOld: # check for new step
                xNewStep = 0
            else:
                xNewStep = 1
            iStepOld = iStep

            # if the agitator is on for greater than its set time turn it off
            if agitator_state():
                fAgitatorCountDown = (fAgitatorCountDown - fStepInterval)
                if (fAgitatorCountDown<0.0):
                    agitator_control(False)
                    storeDataDB.off_agitator(siloID)# rest the control flag on web db
                    print("Agitator Time out Off")  
            else:
                fAgitatorCountDown= fOnTimeSetPoint 
            # update blynk
            blynk.run()
            time.sleep(fStepInterval) # sleep for the step interval
           

    except KeyboardInterrupt:
        print("Good Bye")  
        GPIO.cleanup()  
# ------------------------  Call main Sequence    -----------------------------------------
if __name__ == '__main__':
    mainsequence()
