# General imports
import sys
import os
import logging
from datetime import datetime
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)


# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Prepare directories so they can be reached from anywhere
appDir = os.path.dirname(os.path.realpath(__file__))
assetsDir = os.path.join(appDir, "assets")
# Get required items from other root-level directories
parentDir = os.path.dirname(appDir)
libDir = os.path.join(parentDir, "lib")
if os.path.exists(libDir):
    sys.path.append(libDir)
# Change the below to whatever Waveshare model you have, or add a different display's driver to /lib
from waveshare_epd import (
    epd7in5_V2,
)


# Set design basics
canvasSize = 360
fontSize = int(canvasSize / 2)
angle = 9
bufferX = -22
bufferY = -16


try:
    # Local time
    day = datetime.today().strftime("%d")
    month = datetime.today().strftime("%m")
    year = datetime.today().strftime("%Y")
    timestamp = datetime.today().strftime("%H:%M")
    logging.info(f"Kicking off at {day}/{month}/{year}, {timestamp}...")

    # Load font
    fontFilePath = os.path.join(assetsDir, "JetBrainsMono-Medium.ttf")
    jetBrainsMono = ImageFont.truetype(fontFilePath, fontSize)

    # Start rendering
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    canvas = Image.new("1", (epd.width, epd.height), "black")
    draw = ImageDraw.Draw(canvas)

    # Center grid
    offsetX = int((epd.width - canvasSize) / 2) + bufferX
    offsetY = int((epd.height - canvasSize) / 2) + bufferY

    draw.text(
        (offsetX, offsetY),
        f"{day}{month}",
        font=jetBrainsMono,
        fill="white",
    )

    draw.text(
        (offsetX - (fontSize * 0.15), offsetY + (fontSize * 0.95)),
        year,
        font=jetBrainsMono,
        fill="white",
    )
    canvas = canvas.rotate(angle)

    # Render all of the above to the display
    epd.display(epd.getbuffer(canvas))

    # Put display on pause, keeping what's on screen
    epd.sleep()
    logging.info(f"Finishing printing. Enjoy.")

    # Exit application
    exit()

except IOError as e:
    logging.info(e)

# Exit plan
except KeyboardInterrupt:
    logging.info("Exited.")
    epd7in5_V2.epdconfig.module_exit()
    exit()
