# General imports
import sys
import os
import logging

# Get required items from other root-level directories
libDir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lib"
)

if os.path.exists(libDir):
    sys.path.append(libDir)

from waveshare_epd import (
    epd7in5_V2,
)  # Change to whatever Waveshare model you have, or add your own display's drivers to /lib

# Set up logging
logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd7in5_V2.EPD()

    logging.info("Wiping clean...")
    epd.init()
    epd.Clear()

    epd.sleep()
    logging.info("Going to sleep.")

    # Exit application
    exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("Exited.")
    epd7in5_V2.epdconfig.module_exit()
    exit()
