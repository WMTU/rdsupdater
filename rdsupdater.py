#!/usr/bin/env python

import serial, urllib, re
import xml.etree.ElementTree as ElementTree

def updateRDS():
  rdsport = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    timeout=30,
  )

  # Get data from XML stream
  xml = urllib.urlopen("http://wmtu.mtu.edu/wp-content/wmtu-custom/rssTrackBack.php").read()
  if xml:
    dom = ElementTree.fromstring(xml)
    firstEntry = dom.find("channel").find('item')
    artist = firstEntry.find("artist").text
    song = firstEntry.find("song").text
    sendMe = "%s - %s" % (re.sub("^Song: ", "", song), re.sub("^Artist: ", "", artist))

    # Send the string to RDS injector
    rdsport.open()
    if rdsport.isOpen():
      rdsport.write("TEXT=On Now: %s\n\r" % sendMe )
    rdsport.close()

if __name__ == "__main__":
  updateRDS()
