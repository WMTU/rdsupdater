#!/bin/bash

# some variables to use, for portability
program_name="rdsupdater"
program_bin="/opt/rdsupdater/rdsupdater.py"
program_config="/opt/rdsupdater/config.ini"
debug_log="/opt/rdsupdater/debug.log"
pid_path="/opt/rdsupdater/rdsupdater.pid"

# function to call the command to launch the program
runCmd() { nohup python3 $program_bin --config=$program_config &>> $debug_log& }

# check it the process is running
# check for the PID file existance
# if it doesn't exist then run our script
# if it does exist then check if the PID is real, and if not run it

# ArtworkFetcher
if [ ! -e $pid_path ]; then
    runCmd
else
    PID=`cat $pid_path`
    if ! ps -p $PID > /dev/null; then
        rm $pid_path
        runCmd
    fi
fi
