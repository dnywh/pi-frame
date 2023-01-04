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

# Change the below import to match your display's driver
from waveshare_epd import epd5in83_V2 as display

# Adjust your optical offsets from one place
import layout


# Set design basics
containerSize = layout.size
fontSize = int(containerSize / 2)
angle = 9
offsetX = layout.offsetX - 22  # Offset again for text legibility
offsetY = layout.offsetY - 16  # Offset again for text legibility


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
    epd = display.EPD()
    epd.init()
    epd.Clear()

    canvas = Image.new("1", (epd.width, epd.height), "black")
    draw = ImageDraw.Draw(canvas)

    # Calculate top-left starting position
    startX = offsetX + int((epd.width - containerSize) / 2)
    startY = offsetY + int((epd.height - containerSize) / 2)

    draw.text(
        (startX, startY),
        f"{day}{month}",
        font=jetBrainsMono,
        fill="white",
    )

    draw.text(
        (startX - (fontSize * 0.15), startY + (fontSize * 0.95)),
        year,
        font=jetBrainsMono,
        fill="white",
    )
    canvas = canvas.rotate(angle, resample=Image.NEAREST)

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
    display.epdconfig.module_exit()
    exit()
