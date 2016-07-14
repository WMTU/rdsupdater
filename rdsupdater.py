#!/usr/bin/env python

import serial, time, json, requests

def updateRDS():
  rdsport = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    timeout=30,
  )

  # Get data from json stream
  request_params = {"n": 1, "desc": True, "delay": True}
  json_data = requests.get('http://10.0.1.10/log/api/v1.0/songs', params = request_params).json()
  if json_data["songs"][0]:
    
    sendMe = "%s by %s" % (json_data["songs"][0]["title"], json_data["songs"][0]["artist"])

    # Send the string to RDS injector
    if rdsport.isOpen():
      rdsport.write("TEXT=%s\n\r" % sendMe )
    rdsport.close()

if __name__ == "__main__":
  updateRDS()
