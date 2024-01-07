# AS7341 Spectroradiometer (as7341sr.py) Joe Pardue 11/20/23
# Some of this code is derived from examples provided by Adafruit.com

# ## Import libraries ##
import time
import board
import storage
import busio
import sdcardio
import adafruit_pcf8523
from adafruit_as7341 import AS7341

# ## Setup ##
# ###########

# setup I2C bus for Adafruit sensors  for using
# the built-in STEMMA QT connector on a microcontroller
i2c = board.STEMMA_I2C()

# setup ulti spectral light sensor
sensor = AS7341(i2c)

# setup for RTC
rtc = adafruit_pcf8523.PCF8523(i2c)

# #setup date/time on Adafruit PicowBell#

#  list of days to print to the text file on boot
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# SPI SD_CS pin
SD_CS = board.GP17

#  SPI setup for SD card
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
try:
    storage.mount(vfs, "/sd")
    print("sd card mounted")
except ValueError:
    print("no SD card")

#  to update the RTC, change set_clock to True
#  otherwise RTC will remain set
#  it should only be needed after the initial set
#  if you've removed the coincell battery
set_clock = False

if set_clock:
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023,  3,   6,   00,  00,  00,    0,   -1,    -1))

    print("Setting time to:", t)
    rtc.datetime = t
    print()

#  variable to hold RTC datetime
t = rtc.datetime

time.sleep(1)

#  initial write to the SD card on startup
try:
    with open("/sd/temp.txt", "a") as f:
        #  writes the date
        f.write('The date is {} {}/{}/{}\n'.format(days[t.tm_wday], t.tm_mon, t.tm_mday, t.tm_year))
        #  writes the start time
        f.write('Start time: {}:{}:{}\n'.format(t.tm_hour, t.tm_min, t.tm_sec))
        #  headers for data, comma-delimited
        f.write('Temp,Time\n')
        #  debug statement for REPL
        print("initial write to SD card complete, starting to log")
except ValueError:
    print("initial write to SD card failed - check card")

def bar_graph(read_value):
    scaled = int(read_value / 1000)
    # return "[%5d] " % read_value + (scaled * "*")
    return "%d" % read_value + (scaled * "*")

# f.flush()
# Write first row of .csv file
with open("/sd/csvtest.txt", "a") as f:
    #  writes the date
    f.write('The date is {} {}/{}/{}\n'.format(days[t.tm_wday], t.tm_mon, t.tm_mday, t.tm_year))
    f.write("hour, min, sec, nm415, nm445, nm480, nm515, nm555, nm590, nm630, nm680, Clear, NIR"+"\n")
    print("hour, min, sec, nm415, nm445, nm480, nm515, nm555, nm590, nm630, nm680, Clear, NIR\n")


while True:
    try:
        #  variable for RTC datetime
        t = rtc.datetime
        # sensor values
        nm415 = sensor.channel_415nm
        nm445 = sensor.channel_445nm
        nm480 = sensor.channel_480nm
        nm515 = sensor.channel_515nm
        nm555 = sensor.channel_555nm
        nm590 = sensor.channel_590nm
        nm630 = sensor.channel_630nm
        nm680 = sensor.channel_680nm
        Clear = sensor.channel_clear
        NIR = sensor.channel_nir

        #  append SD card text file
        with open("/sd/csvtest.txt", "a") as f:
            f.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(t.tm_hour,
            t.tm_min, t.tm_sec, nm415, nm445, nm480, nm515, nm555, nm590, nm630, nm680, Clear, NIR))
            print('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(t.tm_hour, t.tm_min, t.tm_sec,
            nm415, nm445, nm480, nm515, nm555, nm590, nm630, nm680, Clear, NIR))
            print("data written to sd card")
        #  repeat every 5 seconds
        time.sleep(5)
    except ValueError:
        print("data error - cannot write to SD card")
        time.sleep(10)

'''
while True:
    print("F1 - 415nm/Violet  %s" % bar_graph(sensor.channel_415nm))
    print("F2 - 445nm//Indigo %s" % bar_graph(sensor.channel_445nm))
    print("F3 - 480nm//Blue   %s" % bar_graph(sensor.channel_480nm))
    print("F4 - 515nm//Cyan   %s" % bar_graph(sensor.channel_515nm))
    print("F5 - 555nm/Green   %s" % bar_graph(sensor.channel_555nm))
    print("F6 - 590nm/Yellow  %s" % bar_graph(sensor.channel_590nm))
    print("F7 - 630nm/Orange  %s" % bar_graph(sensor.channel_630nm))
    print("F8 - 680nm/Red 	%s" % bar_graph(sensor.channel_680nm))
    print("Clear          	%s" % bar_graph(sensor.channel_clear))
    print("Near-IR (NIR)  	%s" % bar_graph(sensor.channel_nir))
    print("\n------------------------------------------------")
    sleep(5)


            sensor.channel_415nm,
            sensor.channel_445nm,
            sensor.channel_480nm,
            sensor.channel_515nm,
            sensor.channel_555nm,
            sensor.channel_590nm,
            sensor.channel_630nm,
            sensor.channel_680nm,
            sensor.channel_clear,
            sensor.channel_nir

            print("415,%s," % nm415)
            print("445nm//Indigo %s" % nm445)
            print("480nm//Blue   %s" % sensor.channel_480nm)
            print("515nm//Cyan   %s" % sensor.channel_515nm)
            print("555nm/Green   %s" % sensor.channel_555nm)
            print("590nm/Yellow  %s" % sensor.channel_590nm)
            print("630nm/Orange  %s" % sensor.channel_630nm)
            print("680nm/Red 	 %s" % sensor.channel_680nm)
            print("Clear          %s" % sensor.channel_clear)
            print("Near-IR (NIR)  %s" % sensor.channel_nir)
            f.write("415nm/Violet  %s" % sensor.channel_415nm)
            f.write("445nm//Indigo %s" % sensor.channel_445nm)
            f.write("480nm//Blue   %s" % sensor.channel_480nm)
            f.write("515nm//Cyan   %s" % sensor.channel_515nm)
            f.write("555nm/Green   %s" % sensor.channel_555nm)
            f.write("590nm/Yellow  %s" % sensor.channel_590nm)
            f.write("630nm/Orange  %s" % sensor.channel_630nm)
            f.write("680nm/Red 	   %s" % sensor.channel_680nm)
            f.write("Clear         %s" % sensor.channel_clear)
            f.write("Near-IR (NIR) %s" % sensor.channel_nir)
'''
