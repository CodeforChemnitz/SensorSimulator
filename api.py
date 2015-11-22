#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask, request, Response
import requests

app = Flask(__name__)

API_HOST = 'http://localhost:5000'
data = {
    "ssid": "",
    "password": "",
    "sensor_id": "",
    "sensor_key": ""
}

@app.route("/")
def getOverview():
    message = "SensorNode\n\n"
    message += "SSID(AP): SensorNode\n"
    message += "IP(AP): "
    message += "YOLOLOLOLO"
    message += "\n\n"
    message += "SSID(local): "
    message += "ToDo"
    message += "\nIP(local): ";
    message += "YOLO"
    message += "\n"

    return message, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/action/register", methods=["POST"])
def actionRegister():
    if "email" not in request.form:
        return "E-Mail not given", 400, {'Content-Type': 'text/plain; charset=utf-8'}

    message = "email:" + request.form["email"] + "\r\n"
    if "name" in request.form:
        message += "name:" + request.form["name"] + "\r\n"

    if False:
        return "Unable to connect to remote server", 500, {'Content-Type': 'text/plain; charset=utf-8'}

    # POST /sensors with message
    r = requests.post(API_HOST + "/sensors", data=message, headers={"X-Sensor-Version": "1"})

    # TODO this is the only difference to the actual code on the microcontroller
    if r.status_code != 200:
        return "Remote server failure: " + str(r.status_code) + ": " + r.content, 500, {'Content-Type': 'text/plain; charset=utf-8'}

    lines = r.content.split("\n")

    # fetch sensor_id and sensor_key
    for line in lines:
        pair = line.split(":", 2)
        if len(pair) == 2:
            if pair[0] == "id":
                data["sensor_id"] = pair[1]
            elif pair[0] == "apikey":
                data["sensor_key"] = pair[1]

    return "Registered", 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/action/restart")
def actionRestart():
    return "reboot", 500, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/action/save")
def actionSave():
    return "Config saved to eeprom", 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route("/info/wifi/sta")
def handleSTA():
    status = {
        "connected": True,
        "ip": "192.168.1.2",
        "netmask": "255.255.255.0"
    }
    return json.dumps(status), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/config/wifi/sta/ssid", methods=["GET", "POST"])
def handleSSID():
    if request.method == "GET":
        if data["ssid"] == "":
            return "SSID not set", 404, {'Content-Type': 'text/plain; charset=utf-8'}
        return data["ssid"]

    if request.form == {}:
        return "No argument given", 400, {'Content-Type': 'text/plain; charset=utf-8'}
    if "ssid" not in request.form:
        return "SSID must at least be 1 character long", 400, {'Content-Type': 'text/plain; charset=utf-8'}

    data['ssid'] = request.form["ssid"]
    return "SSID set", 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/config/wifi/sta/password", methods=["GET", "POST"])
def handlePassword():
    if request.method == "GET":
        if data["password"] == "":
            return "Password not set", 404, {'Content-Type': 'text/plain; charset=utf-8'}
        return data["password"], 200, {'Content-Type': 'text/plain; charset=utf-8'}

    if request.form == {}:
        return "No argument given", 400, {'Content-Type': 'text/plain; charset=utf-8'}

    password = ""
    if "password"  in request.form:
        data['password'] = request.form["password"]

    return "Password set", 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route("/setup", methods=["GET"])
def actionSetup():
    return app.send_static_file("index.html")


@app.route("/setup/js.js")
def actionSetupJS():
    return app.send_static_file("output.min.js")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True, port=5001)
