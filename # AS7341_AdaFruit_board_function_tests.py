# # AS7341_AdaFruit_board_function_tests.py
# Joe Pardue 10/15/24

import time
import board
import busio
from adafruit_as7341 import AS7341

# Initialize I2C bus using STEMMA I2C
i2c = board.STEMMA_I2C()

# Initialize the AS7341 sensor
sensor = AS7341(i2c)

# Functions for sensor operations
def read_channel(channel_number):
    sensor.measurements_enabled = True
    time.sleep(0.5)
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
    value = channel_map.get(channel_number, "Invalid channel")
    sensor.measurements_enabled = False
    return value

def set_gain(gain_value):
    sensor.gain = gain_value
    return f"Gain set to {gain_value}"

def read_light_intensity():
    sensor.measurements_enabled = True
    time.sleep(0.5)
    value = sensor.channel_clear
    sensor.measurements_enabled = False
    return f"Light intensity: {value}"

def set_measurement_mode(mode):
    sensor.measurement_mode = mode
    return f"Measurement mode set to {mode}"

def set_led_current(current_value):
    sensor.led_current = current_value
    return f"LED current set to {current_value} mA"

def enable_flicker_detection(enable):
    sensor.flicker_detection_enabled = enable
    return f"Flicker detection {'enabled' if enable else 'disabled'}"

def read_flicker_status():
    status = sensor.flicker_detected
    return f"Flicker detected: {status}"

def set_aperature_width(width_value):
    sensor.aperture_width = width_value
    return f"Aperture width set to {width_value}"

def enable_spectral_measurement(enable):
    sensor.measurements_enabled = enable
    return f"Spectral measurement {'enabled' if enable else 'disabled'}"

def read_status():
    status = sensor.status
    return f"Sensor status: {status}"

def control_white_led(enable):
    sensor.led = enable
    return f"White LED {'enabled' if enable else 'disabled'}"

def function_details():
    details = {
        'read_channel': "Reads the value from the specified sensor channel (0-9). Pass a channel number to get the corresponding light intensity reading.",
        'set_gain': "Sets the sensor gain to the specified value. Provide a numeric value for the desired gain level.",
        'read_light_intensity': "Reads the overall light intensity from the clear channel. No arguments needed.",
        'set_measurement_mode': "Sets the sensor's measurement mode. Pass the desired mode (e.g., continuous or triggered).",
        'set_led_current': "Sets the LED current to the specified value in milliamps (mA). Provide a numeric value for the LED current.",
        'enable_flicker_detection': "Enables or disables flicker detection. Pass 1 to enable or 0 to disable.",
        'read_flicker_status': "Reads and returns whether flicker is detected by the sensor. No arguments needed.",
        'set_aperature_width': "Sets the aperture width of the sensor. Pass the desired width value.",
        'enable_spectral_measurement': "Enables or disables spectral measurement. Pass 1 to enable or 0 to disable.",
        'read_status': "Reads and returns the current status of the sensor. No arguments needed.",
        'control_white_led': "Turns the white LED on or off. Pass 1 to enable or 0 to disable."
    }
    for command, description in details.items():
        print(f"\033[1m{command}\033[0m: {description}")

# Command handler
commands = {
    'read_channel': read_channel,
    'set_gain': set_gain,
    'read_light_intensity': read_light_intensity,
    'set_measurement_mode': set_measurement_mode,
    'set_led_current': set_led_current,
    'enable_flicker_detection': enable_flicker_detection,
    'read_flicker_status': read_flicker_status,
    'set_aperature_width': set_aperature_width,
    'enable_spectral_measurement': enable_spectral_measurement,
    'read_status': read_status,
    'control_white_led': control_white_led,
    'function_details': function_details
}

# Main loop
while True:
    print("Commands: ")
    print("  read_channel <0-9>")
    print("  set_gain <value>")
    print("  read_light_intensity")
    print("  set_measurement_mode <mode>")
    print("  set_led_current <value>")
    print("  enable_flicker_detection <0|1>")
    print("  read_flicker_status")
    print("  set_aperature_width <value>")
    print("  enable_spectral_measurement <0|1>")
    print("  read_status")
    print("  control_white_led <0|1>")
    print("  function_details")
    user_input = input("Enter command: ")

    # Parse command and argument
    parts = user_input.split()
    command = parts[0]
    arg = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else parts[1] if len(parts) > 1 else None

    # Execute command and log result
    if command in commands:
        response = commands[command](arg) if arg is not None else commands[command]()
    else:
        response = "Invalid command"

    print(response)
    time.sleep(1)
