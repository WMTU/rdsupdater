# import system libraries
import os, json, sys, getopt, configparser, ast
import urllib, urllib.parse, urllib.request
from time import sleep

# import serial to send data to rds units
import serial

class RDSUpdater:
    def __init__(self, check_int, url, args, device):
        # configuration
        self.interval   = check_int
        self.log_url    = url
        self.log_args   = args
        self.device     = device

    # function to fetch the current song data
    def _fetchSong(self):
        # do the request for song data
        try:
            url = self.log_url + '?' + urllib.parse.urlencode(self.log_args)
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

        return { 'title': c_title, 'artist': c_artist, 'album': c_album }

    # function to push an update to the RDS units
    def _update(self, title, artist):
        rdstext = "TEXT={} by {}\n\r".format(title, artist)

        # opens a new serial communication port
        # baud rate of 9600, timeout of 30 seconds
        rdsconn = serial.Serial(self.device, 9600, timeout=30)

        # send the string to RDS injector
        # note: strings must be byte endoded, so use encode() when sending
        if rdsconn.isOpen():
            rdsconn.write(rdstext.encode())
            rdsconn.close()
        else:
            return False
        
        return True

    # function to infinitely run rds updates
    def runUpdater(self):
        c_title     = ""
        c_artist    = ""
        c_album     = ""

        while 1:
            new_song = self._fetchSong()

            if new_song['title'] != c_title or new_song['artist'] != c_artist:
                c_title     = new_song['title']
                c_artist    = new_song['artist']
                c_album     = new_song['album']

                self._update(c_title, c_artist)

            sleep(self.interval)

        return True


# main function, just calls the rds updater method
if __name__ == "__main__":
    # fetch info from the config file
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["config="])

    except (Exception, getopt.GetoptError):
        print("Specify a config file with --config=<file name>")
        sys.exit(1)

    if len(opts) < 1:
        print("Specify a file with --config=<file name>")
        sys.exit(1)

    config_file = None

    for o, a in opts:
        if o == "--config":
            config_file = a

    config = configparser.ConfigParser()
    config.read(config_file)
    pid_path = config['GENERAL']['pid_path']

    # write out a pid file
    # note that this will overwrite an existing pid file
    try:
        pid_file = open(pid_path, 'w')
        pid_file.write(str(os.getpid()) + "\n")
        pid_file.close()
        
    except (Exception, IOError) as e:
        print("IO Error => ", e)

    # update rds
    rds = RDSUpdater(
        int(config['GENERAL']['update_interval']),
        config['GENERAL']['log_url'],
        ast.literal_eval(config['GENERAL']['log_args']),
        config['GENERAL']['serial_device'])

    rds.runUpdater()

    sys.exit(0)
