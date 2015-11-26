# SensorSimulator

This is a simulator to develop the setup client without the actual hardware.

## Requirements

    pip install -r requirements.txt

You also need to run the SensorAPI - https://github.com/CodeforChemnitz/SensorAPI

If this runs on a different host you need to change the variable `API_HOST` in api.py.

## Run

    python api.py

Now you can connect to the simulator on http://localhost:5001.

It behaves like https://git.dinotools.org/poc/SensorNodeESP8266/about/

# WebConfig

The WebConfig is a simple web frontend to configure the sensor node.

## Requirements

- npm
- grunt

Install grunt packages

    npm install

## Development

Rebuild files for the web frontend.

    grunt watch

## Build

Build the files for the web frontend.

    grunt
