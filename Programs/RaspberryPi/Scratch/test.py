from flask import Flask, request, render_template
from flask_cors import CORS
from IOLink import current_values
import json
#read data from io link
jdata = current_values()
print(jdata)
celcius = jdata["temp"]
print("Temp =" + str(celcius))