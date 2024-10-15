# Picowbell_AdaFruit_board_test.py
# Joe Pardue 10/15/24

import time
import board
import busio
from adafruit_ds3231 import DS3231

# Initialize I2C bus using STEMMA I2C
i2c = board.STEMMA_I2C()

# Initialize the PicoW Bell RTC
rtc = DS3231(i2c)

# Functions for RTC operations
def read_time():
    current_time = rtc.datetime
    return f"Current RTC time: {current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday} {current_time.tm_hour:02}:{current_time.tm_min:02}:{current_time.tm_sec:02}"

def set_time(year, month, day, hour, minute, second):
    rtc.datetime = time.struct_time((year, month, day, hour, minute, second, -1, -1, -1))
    return f"RTC time set to {year}-{month}-{day} {hour:02}:{minute:02}:{second:02}"

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
