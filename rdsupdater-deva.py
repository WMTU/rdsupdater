# import system libraries
import urllib, urllib.parse, urllib.request, json

# import telnet to communicate with DEVA RDS
from telnetlib import Telnet

#### CONFIGURATION ####

rds_ip          = '10.10.100.73'
rds_port        = '1024'
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

def updateRDS(telnet_conn, title, artist):
    # format string for the RDS injector
    rdstext = "TEXT={} by {}\n\r".format(title, artist)
    print("=> " + rdstext)

    # send the string to RDS injector
    # note: strings must be byte endoded, so use encode() when sending
    telnet_conn.write(rdstext.encode('ascii') + b"\n")
        
    return True


#### main program ####

print("MANUAL RDS UPDATE PROGRAM")
print("-------------------------\n")

# open up a new telnet connection
with Telnet(rds_ip, rds_port) as tn:

    run = True

    while run == True:
        prompt = input("Update RDS? (y/n) => ")

        if prompt != "y":
            run = False
        
        else:
            run = True
            song_data = fetchSong(log_url, log_args)
            updateRDS(tn, song_data['title'], song_data['artist'])

exit(0)