# 4-Way Intersection Traffic Light Simulator for Raspberry Pi

## Description

This project aims to simulate a 4-way traffic light intersection using a Raspberry Pi and LEDs. Built using Python and utilizing the RPi.GPIO library for hardware interface. The lights switch states according to a predefined schedule.

In the future, I plan to add sensors to dynamically alter the light schedule based on real-time traffic conditions (e.g. a button which can notify the system of a "car" at a corresponding traffic stop).

## Features

- Simulates a 4-way intersection
- Uses RPi.GPIO for GPIO control
- Lights change states based on a predefined schedule

## Future Improvements

- Sensor integration for real-time traffic analysis
- Additional LEDs and sensors for left-turn signals
- Web interface for remote control and monitoring
- Support for additional hardware components (e.g., buzzers for pedestrian signals)

## Requirements

- Raspberry Pi (tested on Pi 4)
- Python 3.x
- RPi.GPIO library
- LEDs (Red, Yellow, Green)
- Jumper wires
- Breadboard
- Resistors

## Installation and Setup

1. Clone this repository into your Raspberry Pi
   ```bash
   git clone https://github.com/ZRay07/4WayTrafficLightSimulator.git
   ```
2. Navigate to the project directory
   ```bash
   cd 4WayTrafficLightSimulator
   ```
3. Install the RPi.GPIO library if you haven't
   ```bash
   pip3 install RPi.GPIO
   ```

## Hardware Setup

1. Connect the LEDs to the Raspberry Pi GPIO pins through the breadboard.
2. Use resistors to limit the current going into the LEDs.
3. Make sure to connect the ground (GND) correctly.

Refer to the `hardware_diagram.JPG` for a complete setup diagram.

## Usage

To run the simulator, execute:

```bash
python3 traffic_light_simulator.py
```

You should see the LEDs change states based on the defined schedule.

## Contributing

Feel free to contribute to this project by forking the repository, making your changes, and creating a pull request. Contributions are highly welcomed!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to the creators of the RPi.GPIO library for making hardware interfacing so much simpler.

## Contact

For any questions or suggestions, feel free to open an issue or contact me directly at [zachray04@gmail.com](mailto:zachray04@gmail.com).
