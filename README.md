# 4-Way Intersection Traffic Light Simulator for Raspberry Pi

## Description

This project aims to simulate the lights of a 4-way intersection using a Raspberry Pi, LEDs, and buttons. Built using Python and utilizing the RPi.GPIO library for hardware interface. The lights switch states according to a combination of a  predefined schedule and button presses.


## Features

- Simulates a 4-way intersection
- Uses RPi.GPIO for GPIO control
- Lights change states based on current state + button press

## Future Improvements

- Sensor integration for real-time traffic analysis
- Additional LEDs and sensors for left-turn signals
- Web interface for remote control and monitoring
- Support for additional hardware components (e.g., buzzers for pedestrian signals)

## Requirements

- Raspberry Pi (tested on Pi 4)
- Python 3.x
- RPi.GPIO library
- 14 x LEDs: 4 x (Red, Yellow, Green) + 2 for button response
- 2 x Push buttons
- Jumper wires
- Breadboard
- Resistors (12 x 220 ohms, 2 x 10k ohms)

## Installation and Setup

1. Clone this repository into your Raspberry Pi
   ```bash
   git clone https://github.com/ZRay07/traffic-light-sim.git
   ```
2. Navigate to the project directory
   ```bash
   cd traffic-light-sim
   ```
3. Install the RPi.GPIO library if you haven't
   ```bash
   pip3 install RPi.GPIO
   ```

## Hardware Setup

1. Connect the LEDs to the Raspberry Pi GPIO pins through the breadboard.
2. Use resistors to limit the current going into the LEDs. (220 ohms)
3. Connect the LEDS to the Raspberry Pi GPIO pins through the breadboard.
4. Use resistors to limit the current going into the push-buttons (10k ohms). This is required to prevent the inputs from floating in either digital 0 or digital 1.
5. It's also worth noting that I used both power rails. When both buttons were attached to one power rail, the callback function associated with the buttons was reading inputs from both channels.
6. Make sure to connect the ground (GND) correctly.

Refer to the [`hardware_diagram.png`](https://github.com/ZRay07/traffic-light-sim/blob/main/hardware_diagram.JPG) for a complete setup diagram.

## Usage

To run the simulator, execute:

```bash
python3 traffic_light_simulator.py schedule
```

You should see the LEDs change states based on the defined schedule.

```bash
python3 traffic_light_simulator.py both
```

You should see the LEDs change states based on the defined schedule. You can press the push buttons to see how these impact the state transitions. For example, if the North and South lights are green, and you press the button corresponding to the North/South side, it will reset the timer which keeps it in that state (5 seconds).

## Discussion and Future Work
### Discussion
This project can be drastically improved and does not accurately reflect the lights of an intersection. The pre-defined schedule is the closest to a real life intersection, however, adding inputs seemed like the most fun to me, but presented a good deal more challenges.

For example, I initially had both push-buttons attached to one power rail. However, I found that pushing one button would sometimes register as both buttons being pushed (I'm still not sure why if someone knows). I fixed this by simply using another 3.3v pin and using the power rail on the other side of the breadboard.

Another thing to note is that this traffic light simulator does not account for a continuous signal from the buttons. In the future, it makes more sense to be able to constantly read from the button while engaging in the schedule. Essentially, the simulator in its current state is only listening for a RISING edge from the input signals. It uses this rising edge and the current state of the system to make a decision on the next state. A more practical solution would take in a continous signal from the button (as if there was a car of lines) vs. (just one car arriving at the traffic light).

### Future work could include:
- Continuous inputs (change buttons to switches or other type of more practical input like photoresistor)
- Pedestrian buttons
- Pedestrian walk signals
- Left turn lanes and sensors
- More robust decision making to ensure each side is getting fair signals

## Contributing

Feel free to contribute to this project by forking the repository, making your changes, and creating a pull request. Contributions are highly welcomed!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to the creators of the RPi.GPIO library for making hardware interfacing so much simpler.

## Contact

For any questions or suggestions, feel free to open an issue or contact me directly at [zachray04@gmail.com](mailto:zachray04@gmail.com).
