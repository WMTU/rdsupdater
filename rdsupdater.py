#!/usr/bin/env python

# import several useful libraries
import serial, time, json, requests, ssl

# location for the json song log data
song_url = 'https://wmtu.fm/log/api/v1.0/songs'

# method for updating RDS data
def updateRDS():
  # opens a new serial communication port
  # baud rate of 9600, timeout of 30 seconds
  rdsconn = serial.Serial('/dev/ttyS0', 9600, timeout=30)

  # pull the current playing song data from the json song log
  request_params = { "n": 1, "desc": True, "delay": True }
  json_data = requests.get( song_url, params = request_params ).json()

  # parse out the actual song now playing text, format it for RDS input
  if json_data["songs"][0]:
    np = "%s by %s" % ( json_data["songs"][0]["title"], json_data["songs"][0]["artist"] )
    rdstext = "TEXT=%s\n\r" % np

    # send the string to RDS injector
    # note: strings must be byte endoded, so use encode() when sending
    if rdsconn.isOpen():
      rdsconn.write( rdstext.encode() )
    rdsconn.close()

# main function, just calls the rds updater method
if __name__ == "__main__":
  updateRDS()
