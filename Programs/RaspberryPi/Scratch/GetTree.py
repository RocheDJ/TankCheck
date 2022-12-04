#!/usr/bin/python3
import requests
api_url = "http://10.15.1.106/gettree"
response = requests.get(api_url)

jsonTree = response.json()

iResponceCode = response.status_code

print("Complete ,  Responce code = "+ str(iResponceCode))
