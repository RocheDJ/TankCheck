#!/usr/bin/python3
from flask import Flask, request, render_template
from flask_cors import CORS
from IOLink import current_values
import json
import RPi.GPIO as GPIO

#create Flask app instance and apply CORS
app = Flask(__name__)
CORS(app)


global xAgitator

#setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, False)

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
    if xAgitator == 0:
        return '{"state":"off"}'
    else:
        return '{"state":"on"}'

# API set agitator value
@app.route('/iolink/agitator',methods=['POST'])
def light_post():
     #ToDo make this live write of  value
    state=request.args.get('state')
    print (state)
    if (state=="on"):
         #ToDo make this live write of  value
        xAgitator = 1
        GPIO.output(10, True)
        return '{"state":"on"}'
    else: 
        #ToDo make this live write of  value
        xAgitator= 0
        GPIO.output(10, False)
        return '{"state":"off"}'



#Run API on port 5000, set debug to True
app.run(host='0.0.0.0', port=5000, debug=True)

