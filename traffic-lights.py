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
import argparse

import RPi.GPIO as GPIO


class TrafficLightController:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.setup_gpio()

    continue_schedule = True
    next_state = "EW-G"

    # Set constants for light delays
    GREEN_DELAY = 5
    YELLOW_DELAY = 3
    RED_DELAY = 1.75

    # Dictionary to hold the mapping of (direction and color) to GPIO pins
    OUTPUT_PIN_MAP = {
        "north_green"  : 3,
        "north_yellow" : 5,
        "north_red"    : 7,

        "south_green"  : 22,
        "south_yellow" : 24,
        "south_red"    : 26,

        "east_green"   : 19,
        "east_yellow"  : 21,
        "east_red"     : 23,

        "west_green"   : 8,
        "west_yellow"  : 10,
        "west_red"     : 12,

        "ns_LED"       : 37,
        "ew_LED"       : 35
    }

    # Dictionary to hold the mapping of (direction and sensor) to GPIO pins
    INP_PIN_MAP = {
        "ns_btn" : 40,
        "ew_btn" : 32
    }

    states = ["EW-G", "EW-Y", "EW-R", "NS-G", "NS-Y", "NS-R"]
    state = "undefined"

    def setup_gpio(self):
        # Initialize the GPIO pins
        GPIO.setup(list(self.OUTPUT_PIN_MAP.values()), GPIO.OUT)
        GPIO.setup(list(self.INP_PIN_MAP.values()), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Attach the ISR to the buttons
        GPIO.add_event_detect(self.INP_PIN_MAP["ns_btn"], GPIO.RISING,
                              callback=self.button_pressed_callback, bouncetime=1000)
        GPIO.add_event_detect(self.INP_PIN_MAP["ew_btn"], GPIO.RISING,
                              callback=self.button_pressed_callback, bouncetime=1000)

    def set_traffic_light(self, direction, color):
        """
        Set the traffic light for a given direction to a specific color.

        Parameters:
        direction (str): Corresponding side. Either {north, south, east, or west}.
        color (str): Color of light. Either {green, yellow, or red}.
        """
        # Turn off all the lights
        for c in ["green", "yellow", "red"]:
            GPIO.output(self.OUTPUT_PIN_MAP[f"{direction}_{c}"], False)

        # Turn on the specified light
        GPIO.output(self.OUTPUT_PIN_MAP[f"{direction}_{color}"], True)

    def set_state(self, state):
        """
        Set the state of the system based on a simple naming convention.
        
        State 1 (EW-G):
                North and South - Red
                East and West   - Green

        State 2 (EW-Y):
                North and South - Red
                East and West   - Yellow

        State 3 (EW-R):
                North and South - Red
                East and West   - Red

        ----------------------------------------------------------

        State 4 (NS-G):
                North and South - Green
                East and West   - Red

        State 5 (NS-Y):
                North and South - Yellow
                East and West   - Red

        State 6 (NS-R):
                North and South - Red
                East and West   - Red

        Repeat from State 1.

        Parameters:
        state (str): State of the system. 6 states. {EW-G, EW-Y, EW-R, NS-G, NS-Y, NS-R}.
        """
        state_mappings = {
            "EW-G": {"east": "green", "west": "green", "north": "red", "south": "red", "delay": self.GREEN_DELAY},
            "EW-Y": {"east": "yellow", "west": "yellow", "north": "red", "south": "red", "delay": self.YELLOW_DELAY},
            "EW-R": {"east": "red", "west": "red", "north": "red", "south": "red", "delay": self.RED_DELAY},
            "NS-G": {"north": "green", "south": "green", "east": "red", "west": "red", "delay": self.GREEN_DELAY},
            "NS-Y": {"north": "yellow", "south": "yellow", "east": "red", "west": "red", "delay": self.YELLOW_DELAY},
            "NS-R": {"north": "red", "south": "red", "east": "red", "west": "red", "delay": self.RED_DELAY},
        }

        settings = state_mappings[state]
        for direction, color in settings.items():
            if direction != "delay":
                self.set_traffic_light(direction, color)
        
        sleep(settings["delay"])

    def button_pressed_callback(self, channel):
        """
        The function to be called when a button is pressed.
        Changes the mode of operation of the traffic lights.

        The new state depends on the current state as well as the inp btn.
        """
        self.continue_schedule = False
        print(f"\n* State when button is pressed: {self.state}")

        if channel == self.INP_PIN_MAP["ew_btn"]:
            GPIO.output(self.OUTPUT_PIN_MAP["ew_LED"], True)
            # Current state is green for east/west directions
            if self.state == "EW-G":
                self.next_state = "EW-G"

            elif self.state == "EW-Y":
                self.next_state = "NS-R"

            elif self.state == "EW-R":
                self.next_state = "NS-R"

            elif self.state == "NS-G":
                self.next_state = "NS-Y"

            elif self.state == "NS-Y":
                self.next_state = "NS-R"

            elif self.state == "NS-R":
                pass

            sleep(0.1)
            GPIO.output(self.OUTPUT_PIN_MAP["ew_LED"], False)
        
        elif channel == self.INP_PIN_MAP["ns_btn"]:
            GPIO.output(self.OUTPUT_PIN_MAP["ns_LED"], True)

            # Current state is green for east/west directions
            if self.state == "EW-G":
                self.next_state = "EW-Y"

            elif self.state == "EW-Y":
                self.next_state = "EW-Y"

            elif self.state == "EW-R":
                pass

            elif self.state == "NS-G":
                self.next_state = "NS-G"

            elif self.state == "NS-Y":
                self.next_state = "EW-R"

            elif self.state == "NS-R":
                self.next_state = "EW-R"

            sleep(0.1)
            GPIO.output(self.OUTPUT_PIN_MAP["ns_LED"], False)

        print(f"* Next state: {self.next_state}")

        self.continue_schedule = True 

    def schedule(self):

        while self.continue_schedule:

            if self.next_state is not None:
                current_state = self.next_state
                # Get the index of the starting state
                for idx, state in enumerate(self.states):
                    if state == current_state:
                        break   # holds value of idx when state matches
                self.next_state = None

            try:
                self.state = self.states[idx]
                print(self.state)
                self.set_state(self.state)

                idx = idx + 1

                if idx >= 6:
                    idx = 0

            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.continue_schedule = False
                GPIO.cleanup()


parser = argparse.ArgumentParser(
                    prog='4-way intersection traffic light simulator',
                    description='Simulate the traffic lights of a 4-way intersection using a Raspberry Pi.')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("change", 
                    type=str,
                    choices= ["schedule", "inp_sensor", "both"],
                    help="define how lights change")
args = parser.parse_args()



if __name__ == "__main__":
    traffic_controller = TrafficLightController()

    if args.change == "schedule":
        print("changing lights based on pre-defined schedule")
        traffic_controller.schedule()

    elif args.change == "inp_sensor":
        print("changing lights based on input sensors")

    elif args.change == "both":
        print("changing lights based on schedule and input sensors")