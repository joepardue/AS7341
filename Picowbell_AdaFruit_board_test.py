# Picowbell_AdaFruit_board.py
# Joe Pardue 10/15/24

import time
import board
import busio
from adafruit_pcf8523 import PCF8523

# Initialize I2C bus using STEMMA I2C
i2c = board.STEMMA_I2C()

# Initialize the PicoW Bell RTC
try:
    rtc = PCF8523.PCF8523(i2c)
    print("PCF8523 RTC detected successfully.")
except ValueError:
    print("PCF8523 RTC not found on the I2C bus.")

# Functions for RTC operations
def read_time():
    try:
        current_time = rtc.datetime
        return f"Current RTC time: {current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday} {current_time.tm_hour:02}:{current_time.tm_min:02}:{current_time.tm_sec:02}"
    except Exception as e:
        return f"Error reading time: {e}"

def set_time(year, month, day, hour, minute, second):
    try:
        rtc.datetime = time.struct_time((year, month, day, hour, minute, second, 0, 0, -1))
        return f"RTC time set to {year}-{month}-{day} {hour:02}:{minute:02}:{second:02}"
    except Exception as e:
        return f"Error setting time: {e}"

def function_details():
    details = {
        'read_time': "Reads the current time from the RTC. No arguments needed.",
        'set_time': "Sets the RTC time. Pass year, month, day, hour, minute, and second as arguments."
    }
    for command, description in details.items():
        print(f"\033[1m{command}\033[0m: {description}")

# Command handler
commands = {
    'read_time': read_time,
    'set_time': set_time,
    'function_details': function_details
}

# Main loop
while True:
    print("Commands: ")
    print("  read_time")
    print("  set_time <year> <month> <day> <hour> <minute> <second>")
    print("  function_details")
    user_input = input("Enter command: ")

    # Parse command and argument
    parts = user_input.split()
    command = parts[0]
    args = [int(part) if part.isdigit() else part for part in parts[1:]]

    # Execute command and log result
    if command in commands:
        response = commands[command](*args) if args else commands[command]()
    else:
        response = "Invalid command"

    print(response)
    time.sleep(1)
