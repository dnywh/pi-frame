# General imports
import sys
import os
import logging
import math
from datetime import datetime
import random  # For randomly choosing an image

from PIL import Image, ImageDraw

# Set up logging
logging.basicConfig(level=logging.DEBUG)
# Set PIL to not log so much
logging.getLogger("PIL").setLevel(logging.INFO)

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


# Design parameters
margin = 28
maskWidth = layout.maskWidth - margin
maskHeight = layout.maskHeight - margin
offsetX = layout.offsetX
offsetY = layout.offsetY
cellGap = 6


def crossedOffCell(x, y, img):
    # Drop in a Sharpie-like scribble image
    canvas.paste(img, (int(x - (imageExcess / 2)), int(y - (imageExcess / 2))))
    # Draw outline for surrounding rectangle
    draw.line([(x, y), (x + cellSize, y)], fill="black", width=1)
    draw.line([(x + cellSize, y), (x + cellSize, y + cellSize)], fill="black", width=1)
    draw.line([(x + cellSize, y + cellSize), (x, y + cellSize)], fill="black", width=1)
    draw.line([(x, y + cellSize), (x, y)], fill="black", width=1)


try:
    timeStampNice = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Kicking off at {timeStampNice}")
    # Calculate current day of year and amount of days in current year
    thisYear = datetime.today().year
    firstDayOfYear = datetime(thisYear, 1, 1)
    lastDayOfYear = datetime(thisYear, 12, 31)
    currentDayOfYear = datetime.now().timetuple().tm_yday
    totalDaysThisYear = (lastDayOfYear - firstDayOfYear).days + 1
    daysPassed = currentDayOfYear - 1
    logging.info(f"Crossing off {daysPassed} days of {totalDaysThisYear}")

    # Create a square grid based on year information
    cols = math.ceil(math.sqrt(totalDaysThisYear))
    rows = cols
    # Calculate how many rows are excess as a result of the square shape
    excessRows = math.trunc(((cols * rows - totalDaysThisYear) / rows))
    maxCellSize = int(maskWidth / cols)
    cellSize = maxCellSize - cellGap
    imageExcess = int(cellSize * 0.25)

    # Prepare images
    amountOfAssets = len(
        [
            name
            for name in os.listdir(assetsDir)
            if os.path.isfile(os.path.join(assetsDir, name))
        ]
    )

    possibleImg = []
    for i in range(amountOfAssets):
        img = Image.open(os.path.join(assetsDir, f"scribble-{i + 1:02d}.gif")).resize(
            (cellSize + imageExcess, cellSize + imageExcess)
        )
        possibleImg.append(img)

    # Start rendering
    epd = display.EPD()
    epd.init()
    epd.Clear()

    canvas = Image.new("1", (epd.width, epd.height), "white")
    draw = ImageDraw.Draw(canvas)

    # Calculate top-left starting position
    startX = (
        offsetX + int((epd.width - (cols * (cellSize + cellGap))) / 2) + (cellGap / 2)
    )
    startY = (
        offsetY
        + int((epd.height - (rows * (cellSize + cellGap))) / 2)
        + (cellGap / 2)
        + ((excessRows * cellSize) / 2)
        + (cellGap / 2)
    )

    # Prepare starting positions
    gridIndex = 0
    itemX = 0
    itemY = 0

    # Traverse through rows top to bottom
    for kk in range(rows):
        # Traverse through cols left to right
        for jj in range(cols):
            cellX = startX + itemX
            cellY = startY + itemY
            # Check if cell is within days of day
            if gridIndex + 1 <= totalDaysThisYear:
                # This cell is within the amount of days of the year (e.g. <=366 for a leap year)
                # Draw container rectangle
                draw.rectangle(
                    [(cellX, cellY), (cellX + cellSize, cellY + cellSize)],
                    fill="white",
                    outline="black",
                    width=1,
                )
                # Check if cell is day in past
                if gridIndex + 1 <= daysPassed:
                    # This day has already passed
                    # Fill rectangle
                    img = random.choice(possibleImg)
                    crossedOffCell(cellX, cellY, img)
                # else:
                # This day hasn't passed yet
            # Move to the next column in the row
            itemX += cellSize + cellGap
            # Store what gridIndex we're up to
            gridIndex += 1
        # Go to next row down
        itemY += cellSize + cellGap
        # Go to first column on left
        itemX = 0

    # Render all of the above to the display
    epd.display(epd.getbuffer(canvas))

    # Put display on pause, keeping what's on screen
    epd.sleep()
    logging.info(f"Finishing printing. Enjoy.")

    # Exit application
    exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("Exited.")
    display.epdconfig.module_exit()
    exit()
