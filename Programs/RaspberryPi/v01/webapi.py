#!/usr/bin/python3
#------------------------------------------------------------------------------------------------
# By: David Roche based on SETU LAB exercieses 
# Date: December 2022
# Description : Local Web API for Tank control and monitering on Raspberry Pi
#------------------------------------------------------------------------------------------------
from flask import Flask, request, render_template
from flask_cors import CORS
from IOLink import current_values
import json
import RPi.GPIO as GPIO
from time import sleep
#create Flask app instance and apply CORS

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates', static_folder='staticfiles')
CORS(app)

xAgitator  = 0

iIOChannel =26



# local index page
@app.route('/') 
def index():
      #read data from io link
      jdata = current_values()
      celcius = jdata["temp"]
      fahrenheit = round(1.8 * celcius + 32, 2)
      level = jdata["level"]
      if level == 8189:
        level = "FULL"
      return render_template('status.html', celcius=celcius, fahrenheit=fahrenheit,level=level)

# API get values
@app.route('/iolink/environment',methods=['GET'])
def current_environment():
    msg = current_values()
    return str(msg)+"\n"

# API Get agitator Setting
@app.route('/iolink/agitator',methods=['GET'])
def agitator_get():
    #ToDo make this live read of current value
    state = GPIO.input(iIOChannel)
    if state:
        return '{"state":"on"}'
    else:
        return '{"state":"off"}'

# API set agitator value
@app.route('/iolink/agitator',methods=['POST'])
def light_post():
     #ToDo make this live write of  value
    state=request.args.get('state')
    print (state)
    if (state=="on"):
         #ToDo make this live write of  value
        xAgitator = 1
        GPIO.output(iIOChannel, True)
        return '{"state":"on"}'
    else: 
        #ToDo make this live write of  value
        xAgitator= 0
        GPIO.output(iIOChannel, False)
        return '{"state":"off"}'



#Run API on port 5000, set debug to True
def runWebAPI(fDelay,xDebugMode):
    sleep(fDelay)
    app.run(host='0.0.0.0', port=5000, debug=xDebugMode)