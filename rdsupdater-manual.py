# import system libraries
import os, json, sys, getopt, configparser, ast
import urllib, urllib.parse, urllib.request
from time import sleep

# import serial to send data to rds units
import serial

#### CONFIGURATION ####

serial_device   = /dev/ttyUSB0
log_url         = "https://log.wmtu.fm/api/2.0/log"
log_args        = { 'n': '1', 'delay': 'true' }


#### helper functions ####

# fetch the current song information
def fetchSong(log_url, log_args):
    # do the request for song data
    try:
        url = log_url + '?' + urllib.parse.urlencode(log_args)
        request = urllib.request.Request(url, headers={'User-Agent': 'RDS-Updater'})
        data = urllib.request.urlopen(request).read()
        data = json.loads(data.decode('utf-8'))
            
    except (Exception, urllib.error.HTTPError) as e:
        print("HTTP Error => ", e)
        data = [{'song': '91.9FM', 'artist': 'WMTU', 'album': 'WMTU'}]
    except (Exception, urllib.error.URLError) as e:
        print("URL Error => ", e)
        data = [{'song': '91.9FM', 'artist': 'WMTU', 'album': 'WMTU'}]

    # set current song
    c_title     = data[0]['song']
    c_artist    = data[0]['artist']
    c_album     = data[0]['album']

    print("=> CURRENT SONG: {} by {}".format(c_title, c_artist))

    return { 'title': c_title, 'artist': c_artist, 'album': c_album }

def updateRDS(rdsconn, title, artist):
    # format string for the RDS injector
    rdstext = "TEXT={} by {}\n\r".format(title, artist)

    # send the string to RDS injector
    # note: strings must be byte endoded, so use encode() when sending
    if rdsconn.isOpen():
        print("=> PLAIN TXT: " + rdstext)
        print("=> ENCOD TXT: " + rdstext.encode())
        rdsconn.write(rdstext.encode())
        rdsconn.close()
    else:
        return False
        
    return True


#### main program ####

print("MANUAL RDS UPDATE PROGRAM")
print("-------------------------\n")

# opens a new serial communication port
# baud rate of 9600, timeout of 30 seconds
serial_conn = serial.Serial(serial_device, 9600, timeout=30)

run = True

while run == True:
    prompt = input("Update RDS? (Y/N) => ")

    if prompt != "Y":
        run = False
    
    else:
        run = True
        song_data = fetchSong(log_url, log_args)
        updateRDS(serial_conn, song_data['title'], song_data['artist'])

print("\n-------------------------")

exit(0)