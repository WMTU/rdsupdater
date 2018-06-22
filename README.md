
# rdsupdater

Script for periodically updating a RDS injector over serial.

## Setup

* Python 3
* pySerial needs to be installed
* run using a cron job

  ```bash
  # m h  dom mon dow   command
    * *   *   *   *    python3 /opt/rdsupdater/rdsupdater.py
  ```

* Must be run with a ROOT user in order to access the required serial system device!

## Changelog

* June 22, 2018
  * Updated for Python 3 and now works with SSL.
  * Updated string formatting to work with newer versions of pySerial.
  * Added numerous comments to make it easier to understand code.
  * Updated the README with some more detail.
