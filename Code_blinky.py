import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True  # Turn on the LED
    time.sleep(2)
    led.value = False  # Turn off the LED
    time.sleep(2)
