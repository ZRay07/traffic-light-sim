#######
# This file is meant to simulate a 4-way intersection with traffic lights
#
#
#
#######

from time import sleep

import RPi.GPIO as GPIO


# BOARD mode simply means using pins numbered 1-40 as compared to
# 	BCM where you are using channel numbers on the Broadcom SOC
GPIO.setmode(GPIO.BOARD)

# Set the pins which will correspond to the traffic lights
output_leds = [3, 5, 7, 8, 10, 12, 19, 21, 23, 22, 24, 26]
GPIO.setup(output_leds, GPIO.OUT)

def green_east_and_west():
    GPIO.output(22, True)
    GPIO.output(24, False)
    GPIO.output(26, False)

    GPIO.output(19, True)
    GPIO.output(21, False)
    GPIO.output(23, False)


def yellow_east_and_west():
    GPIO.output(22, False)
    GPIO.output(24, True)
    GPIO.output(26, False)

    GPIO.output(19, False)
    GPIO.output(21, True)
    GPIO.output(23, False)



def red_east_and_west():
    GPIO.output(22, False)
    GPIO.output(24, False)
    GPIO.output(26, True)

    GPIO.output(19, False)
    GPIO.output(21, False)
    GPIO.output(23, True)


def green_north_and_south():
    GPIO.output(8, True)
    GPIO.output(10, False)
    GPIO.output(12, False)

    GPIO.output(3, True)
    GPIO.output(5, False)
    GPIO.output(7, False)

def yellow_north_and_south():
    GPIO.output(8, False)
    GPIO.output(10, True)
    GPIO.output(12, False)

    GPIO.output(3, False)
    GPIO.output(5, True)
    GPIO.output(7, False)

def red_north_and_south():
    GPIO.output(8, False)
    GPIO.output(10, False)
    GPIO.output(12, True)

    GPIO.output(3, False)
    GPIO.output(5, False)
    GPIO.output(7, True)

def main():

    try:
        while True:

        ########
        # At the start of the intersection simulation,
	# the East and West sides will have green lights.
	# and the North and South sides will have red lights.
	########

            red_north_and_south()
            green_east_and_west()

            sleep(5)

            yellow_east_and_west()

            sleep(3)

            red_east_and_west()

            sleep(1.75)

            green_north_and_south()

            sleep(5)

            yellow_north_and_south()

            sleep(3)

            red_north_and_south()

            sleep(1.75)

    except KeyboardInterrupt:
        GPIO.output(output_leds, False)

if __name__ == "__main__":
    main()
