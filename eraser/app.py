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

# Change the below import to match your display's driver
from waveshare_epd import epd5in83_V2 as display

# Set up logging
logging.basicConfig(level=logging.DEBUG)

try:
    epd = display.EPD()

    logging.info("Wiping clean...")
    epd.init()
    epd.Clear()

    epd.sleep()
    logging.info("Clean as a whistle. Enjoy")

    # Exit application
    exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("Exited.")
    display.epdconfig.module_exit()
    exit()
