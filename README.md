# rdsupdater

Python 3 script for periodically updating a RDS injector over serial.

## Setup

* install pyserial with pip
* run using a cron job

  ```bash
  # m h  dom mon dow   command
    * *   *   *   *    bash /opt/rdsupdater/rdsupdater-check.sh
  ```

* Must be run with a ROOT user in order to access the required serial system device!

## Changelog

October 11, 2019

* Rewrite for use as a daemon process
* Now uses a config file for easier customization

June 22, 2018

* Updated for Python 3 and now works with SSL.
* Updated string formatting to work with newer versions of pySerial.
* Added numerous comments to make it easier to understand code.
* Updated the README with some more detail.
