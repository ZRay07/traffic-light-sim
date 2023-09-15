"""
This file simulates traffic lights at a 4-way intersection using a Raspberry Pi.

The Raspberry Pi's GPIO pins are used to control the LEDs that represent traffic lights.

TO-DO: [BELOW] ADD INPUT SENSORS TO SYSTEM
If no input to the system, the lights operate on a pre-defined schedule
    Buttons on the south side and the east side allow for the system to simulate a "car" being there
If there is a car at one of the sides, the lights will switch and allow the cars to pass for
    as long as the button is pressed down
"""
from time import sleep
from threading import Thread

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Use the BOARD numbering system for GPIO pins
GPIO.setmode(GPIO.BOARD)

# Dictionary to hold the mapping of (direction and color) to GPIO pins
OUTPUT_PIN_MAP = {
    "north_green"  : 3,
    "north_yellow" : 5,
    "north_red"    : 7,

    "south_green"  : 8,
    "south_yellow" : 10,
    "south_red"    : 12,

    "east_green"   : 19,
    "east_yellow"  : 21,
    "east_red"     : 23,

    "west_green"   : 22,
    "west_yellow"  : 24,
    "west_red"     : 26,

    "ns_LED"       : 37,
    "ew_LED"       : 35
}

# Dictionary to hold the mapping of (direction and sensor) to GPIO pins
INP_PIN_MAP = {
    "ns_btn" : 40,
    "ew_btn" : 38
}

# Initialize the GPIO pins
GPIO.setup(list(OUTPUT_PIN_MAP.values()), GPIO.OUT)
GPIO.setup(list(INP_PIN_MAP.values()), GPIO.IN)

# Set constants for light delays
GREEN_DELAY = 5
YELLOW_DELAY = 3
RED_DELAY = 1.75



def set_traffic_light(direction, color):
    """
    Set the traffic light for a given direction to a specific color.

    Parameters:
	direction (str): Corresponding side. Either {north, south, east, or west}.
	color (str): Color of light. Either {green, yellow, or red}.
    """
    # Turn off all the lights for the given direction
    for c in ["green", "yellow", "red"]:
        GPIO.output(OUTPUT_PIN_MAP[f"{direction}_{c}"], False)

    # Turn on the specified light
    GPIO.output(OUTPUT_PIN_MAP[f"{direction}_{color}"], True)


def listen_for_ns_car():
    if not GPIO.input(INP_PIN_MAP["ns_btn"]):
        GPIO.output(INP_PIN_MAP["ns_LED"], True)

def main():

    ns_thread = Thread(target=listen_for_ns_car)
    ns_thread.run()

    try:
        while True:
        ########
        # At the start of the intersection simulation,
	# the East and West sides will have green lights.
	# and the North and South sides will have red lights.
	########
            set_traffic_light("east", "green")
            set_traffic_light("west", "green")
            set_traffic_light("north", "red")
            set_traffic_light("south", "red")

            sleep(GREEN_DELAY)

            set_traffic_light("east", "yellow")
            set_traffic_light("west", "yellow")

            sleep(YELLOW_DELAY)

            set_traffic_light("east", "red")
            set_traffic_light("west", "red")

            sleep(RED_DELAY)

            set_traffic_light("east", "red")
            set_traffic_light("west", "red")
            set_traffic_light("north", "green")
            set_traffic_light("south", "green")

            sleep(GREEN_DELAY)

            set_traffic_light("north", "yellow")
            set_traffic_light("south", "yellow")

            sleep(YELLOW_DELAY)

            set_traffic_light("north", "red")
            set_traffic_light("south", "red")

            sleep(RED_DELAY)

    except KeyboardInterrupt:
        GPIO.output(list(OUTPUT_PIN_MAP.values()), False)

if __name__ == "__main__":
    main()
