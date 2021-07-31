#!/usr/bin/env python3

import logging
from datetime import datetime
from time import sleep
from dragino import Dragino

def encode_gps(gga):
    return '{0},{1}'.format(
        '{:.5f}'.format(gga.longitude),
        '{:.5f}'.format(gga.latitude),
    )


# add logfile
logLevel=logging.DEBUG
logging.basicConfig(filename="send_gps.log", format='%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s', level=logLevel)

D = Dragino("dragino.ini", logging_level=logLevel)

gps = D.get_gps()

if (gps.gps_qual == 0):
    D.logger.info("No GPS lock, skipping transmission")
    exit()


D.join()
while not D.registered():
    print("Waiting for JOIN ACCEPT")
    sleep(2)

encoded_gps = encode_gps(gps)
D.send(encoded_gps)
start = datetime.utcnow()
while D.transmitting:
    pass
end = datetime.utcnow()

D.cleanup()
