#!/usr/bin/env python

import serial, urllib, re
import json

def updateRDS():
  rdsport = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    timeout=30,
  )

  # Get data from json stream
  json = json.loads(urllib.urlopen("http://wmtu.mtu.edu/php/songfeed.php").read())
  if json:
    
    sendMe = "%s - %s" % (json[0]["song_name"], json[0]["artist"])

    # Send the string to RDS injector
    rdsport.open()
    if rdsport.isOpen():
      rdsport.write("TEXT=On Now: %s\n\r" % sendMe )
    rdsport.close()

if __name__ == "__main__":
  updateRDS()
