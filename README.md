# Pi Frame

![Pi Frame Sequence.gif](https://res.cloudinary.com/dannywhite/image/upload/v1672984819/github/pi-frame-sequence.gif.gif)

Pi Frame is a lightweight starter kit for printing timely data or art (or both) to an e-ink/e-Paper display. It’s like your own newspaper, except that it updates itself however often you like and with whatever content you find interesting.

## Prerequisites

To run Pi Frame you need to first:

1. Join a Wi-Fi network on your Raspberry Pi
2. Enable SSH on your Raspberry Pi
3. Plug in a Waveshare e-Paper or similar display to your Raspberry Pi

Waveshare displays require some additional setup. See the [Hardware Connection](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Hardware_Connection) and [Python](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Python) sections of your model’s manual.

## Get started

Copy all the contents of this Pi Frame repository over to the main directory of your Raspberry Pi. Or, at a minimum, bring over the _[lib](https://github.com/dnywh/pi-frame/tree/main/lib)_ directory and that of either [Date Stamp](https://github.com/dnywh/pi-frame/tree/main/date-stamp) or [Year Progress](https://github.com/dnywh/pi-frame/tree/main/year-progress).

The _[lib](https://github.com/dnywh/pi-frame/tree/main/lib)_ directory includes vendored copies of each Waveshare display driver taken from the official [repository](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd). Make sure to add your own display’s driver to _[lib](https://github.com/dnywh/pi-frame/tree/main/lib)_ if you aren’t using a Waveshare display.

Now you just need to tell Pi Frame which display to expect and download any required packages.

### Set the display driver

Look for this line as the last import in each Pi Frame app:

```python
from waveshare_epd import epd5in83_V2 as display
```

Swap out the `epd5in83_V2` for your Waveshare e-Paper display driver in the _[lib](https://github.com/dnywh/pi-frame/tree/main/lib)_ directory. Non-Waveshare displays should be imported here too, although you’ll need to make display-specific adjustments needed wherever `display` is called further on.

### Install required packages

See _[requirements.txt](https://github.com/dnywh/pi-frame/blob/main/requirements.txt)_ for a short list of packages required for Pi Frame’s built-in demo apps. Only `python3-pil` is required as of writing this.

Install each package on your Raspberry Pi using `sudo apt-get`. Here’s an example:

```bash
sudo apt-get update
sudo apt-get install python3-pil
```

### Run your first app

Run Pi Frame apps just like you would any other Python file on a Raspberry Pi:

```bash
# Run the Date Stamp demo app
cd date-stamp
python3 app.py

# Or run the Year Progress demo app
cd year-progress
python3 app.py
```

Pi Frame is noisy by default. Look for the results in Terminal.

### Install and run other apps

Check out the list of [apps](#apps) below. Just like what’s been mentioned: copy one of them over to your Raspberry Pi’s main directory, replace the driver name in its import, install the required packages, and run.

---

## **Apps**

Here is a list of apps I’ve built to make Pi Frame my own. Read on for how to [schedule](#scheduling) these apps at certain hours of the day and/or days of the week.

### **Included**

The Pi Frame repository is limited to three basic apps in order to keep its complexity to a minimum. None of these apps require any authentication or setup beyond some minimal package installation, which is covered [above](#install-required-packages).

| Name                                                                       | Description                                                    |
| -------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [Date Stamp](https://github.com/dnywh/pi-frame/tree/main/date-stamp)       | Prints today’s date according to the time zone set on your Pi. |
| [Year Progress](https://github.com/dnywh/pi-frame/tree/main/year-progress) | Prints a how far through the year we are.                      |
| [Eraser](https://github.com/dnywh/pi-frame/tree/main/eraser)               | Wipes the Pi’s screen clean.                                   |

### External

These apps are why Pi Frame exists: they’re all things I wanted to track or see throughout the day. Each of them require an internet connect and package installation. They have optional customisation for your location and preferences.

| Name                                            | Description                                                          |
| ----------------------------------------------- | -------------------------------------------------------------------- |
| [Where ISS](https://github.com/dnywh/where-iss) | Prints what the International Space Station sees of Earth.           |
| [Art Press](https://github.com/dnywh/art-press) | Prints a random item from the Art Institute of Chicago's collection. |
| [Surf Grid](https://github.com/dnywh/surf-grid) | Prints the day's surf report in the style of Kōhei Sugiura.          |

### **Ideas**

These are external projects that I think could be nice for Pi Frame.

| Name                                                  | Description                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [SlowMovie](https://github.com/TomWhitwell/SlowMovie) | A [Very Slow Movie Player](https://medium.com/s/story/very-slow-movie-player-499f76c48b62) for Raspberry Pi. |

## Scheduling

Pi Frame relies on [cron](https://en.wikipedia.org/wiki/Cron) to schedule apps to run at certain hours of the day and/or days of the week. Make sure your Raspberry Pi’s time zone is correct before setting up cron jobs. You can read how to do this in the [appendix](#appendix).

First, give cron permission to use the _launcher_ file for each app:

```bash
# Art Press
chmod 755 art-press/launcher.sh
# Year Progress
chmod 755 year-progress/launcher.sh
## And so on...
```

Repeat this `chmod 755` line for each app you’d like to have on a schedule.

Second, set up the actual crontab process. Make sure you include the `sudo` in this command:

```bash
sudo crontab -e
```

This will open up the _crontab_ file that needs to be filled out. Refer to the _[crontab.example](https://github.com/dnywh/pi-frame/blob/main/crontab.example)_ file in this repository for a starting point and [crontab.guru](https://crontab.guru) to create custom schedules. Paste in (or write) your cron jobs in the crontab. Save it out.

Pi Frame’s _[crontab.example](https://github.com/dnywh/pi-frame/blob/main/crontab.example)_ includes instructions for cron to save logs (including errors) to a _cronlog.log_ file at your Raspberry Pi’s main directory. This _cronlog.log_ will be overwritten each time cron runs one of the scheduled jobstasks.

## Layout

Pi Frame apps get their size and optical offset positions from the _[layout.py](https://github.com/dnywh/pi-frame/blob/main/lib/layout.py)_ module. I recommend you first set up your display how you like within a picture frame (with a window mat cut from thick paper stock) before adjusting these values.

External apps such as [Where ISS](https://github.com/dnywh/where-iss), [Art Press](https://github.com/dnywh/art-press), and [Surf Grid](https://github.com/dnywh/surf-grid) have their layout values hardcoded in the interest of portability. You’ll need to remove these hardcoded values and un-comment the _[layout.py](https://github.com/dnywh/pi-frame/blob/main/lib/layout.py)_ module import and references in order to use the shared values.

---

## Feedback

I’d love to hear how you go with this project. Drop any issues as [GitHub issues](https://github.com/dnywh/pi-frame/issues/new) and [email me](mailto:endless.paces-03@icloud.com) for anything else.

## See also

Check out Scott Kildall‘s [write-up](https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/) on cron, scheduling, and Python file launchers on Rasperry Pi. Also check out Michael Klements‘ [tutorial](https://www.the-diy-life.com/make-a-youtube-subscriber-counter-using-an-e-ink-display-and-a-raspberry-pi-zero-w/) on Waveshare displays, APIs, and Raspberry Pi.

---

## Appendix

### Burn-in

Waveshare recommends you update the display’s contents at least once every 24 hours to prevent burn-in. I don’t keep anything longer than 12 hours to be safe. I also [schedule](#scheduling) the Eraser app every night between sleeping hours.

### Set your Pi’s time zone

I recommend you use your local time zone for [scheduling](#scheduling) apps. You can do this with a simple command on your Raspberry Pi:

```bash
date
```

Here’s how to edit your time zone if it isn’t accurate:

```bash
sudo raspi-config
```

Navigate down to _Localisation Options_ and then _Timezone_ to find yours. UTC is tucked away under _None of the above_.

### Sending files to your Raspberry Pi

I like using [Transmit](https://panic.com/transmit/) to transfer files to and from the Pi. You could also use `scp`. Here are some basic commands:

**Upload a whole directory with `scp`**

Useful for installing Pi Frame apps.

```bash

# Uploading the `app-name` directory to your Pi at an IP address
scp -r app-name/ pi@192.168.20.12:

# Uploading the `app-name` directory to your Pi at its hostname
scp -r app-name/ pi@raspberrypi:

```

The rest of these instructions will assume you are using the `pi@raspberrypi` hostname.

**Upload a single file with `scp`**

Useful for uploading Pi Frame app edits.

```bash
# Copy a file from the `app-name` directory from your computer to your Pi
scp app-name/app.py pi@raspberrypi:app-name/app.py
```

**Delete a whole directory via `scp`**

```bash
# Danger!
# This irreversibly deletes the entire folder and its contents
sudo rm -rf app-name
```

### Using a Raspbery Pi Pico W

I find it doesn’t have enough oompf to make anything practical. Let me know if you find otherwise.
