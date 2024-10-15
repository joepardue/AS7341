# AS7341_function_test_framework.py
# Joe Pardue 10/15/24

import time
import board
import busio
from adafruit_as7341 import AS7341

# Initialize I2C bus using STEMMA I2C
i2c = board.STEMMA_I2C()

# Initialize the AS7341 sensor
sensor = AS7341(i2c)

# Function to read a specific channel
def read_channel(channel_number):
    try:
        sensor.measurements_enabled = True  # Enable measurements
        time.sleep(0.5)  # Small delay for measurement
        channel_map = {
            0: sensor.channel_415nm,
            1: sensor.channel_445nm,
            2: sensor.channel_480nm,
            3: sensor.channel_515nm,
            4: sensor.channel_555nm,
            5: sensor.channel_590nm,
            6: sensor.channel_630nm,
            7: sensor.channel_680nm,
            8: sensor.channel_clear,
            9: sensor.channel_nir
        }
        value = channel_map[channel_number]
        sensor.measurements_enabled = False  # Disable measurements
        return f"Channel {channel_number} value: {value}"
    except KeyError:
        return "Invalid channel"
    except AttributeError:
        return "Channel reading error"

# Function to set the gain of the sensor
def set_gain(gain_value):
    sensor.gain = gain_value
    return f"Gain set to {gain_value}"

# Function to calculate an approximation of light intensity using the clear channel
def read_light_intensity():
    sensor.measurements_enabled = True
    time.sleep(0.5)  # Small delay for measurement
    value = sensor.channel_clear  # Use clear channel for light intensity approximation
    sensor.measurements_enabled = False
    return f"Approximate light intensity (from clear channel): {value}"

# Function to reset the sensor (additional test function)
def reset_sensor():
    sensor.reset()
    return "Sensor has been reset"

# Define command options in a switch-like dictionary
commands = {
    'read_channel': read_channel,
    'set_gain': set_gain,
    'read_light_intensity': read_light_intensity,
    'reset_sensor': reset_sensor
}

# Input handling function
def handle_command(command, arg=None):
    if command in commands:
        if arg is not None:
            return commands[command](arg)
        else:
            return commands[command]()
    else:
        return "Invalid command"

# Main loop to handle user input and execute commands
while True:
    print("Available commands: read_channel, set_gain, read_light_intensity, reset_sensor")
    user_input = input("Enter command: ")

    # Parse command and argument if available
    parts = user_input.split()
    command = parts[0]
    arg = int(parts[1]) if len(parts) > 1 else None

    # Execute command and print result
    result = handle_command(command, arg)
    print(result)

    time.sleep(1)
