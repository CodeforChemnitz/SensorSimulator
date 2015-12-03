#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask, request, Response
import requests

app = Flask(__name__)

API_HOST = 'http://localhost:5000'
data = {
    "api_hostname": "",
    "api_port": 0,
    "ssid": "",
    "password": "",
    "sensor_api_id": "",
    "sensor_api_key": "",
    "sensor_config": {}
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
    email = request.form.get("email")
    if email is None or email.strip() == "":
        return "E-Mail not given", 400, {"Content-Type": "text/plain"}

    register_info = {
        "email": email
    }

    name = request.form.get("name")
    if name is not None and name.strip() != "":
        register_info["name"] = name

    if False:
        return "Unable to connect to remote server", 500, {'Content-Type': 'text/plain'}

    # POST /sensors with message
    r = requests.post(API_HOST + "/sensors", json=register_info, headers={"X-Sensor-Version": "1"})

    # TODO this is the only difference to the actual code on the microcontroller
    if r.status_code != 200:
        return "Remote server failure: " + str(r.status_code) + ": " + r.content.decode("utf-8"), 500, {'Content-Type': 'text/plain; charset=utf-8'}

    api_credentials = r.content.decode("utf-8")
    api_credentials = json.loads(api_credentials)

    if "id" not in api_credentials or "key" not in api_credentials:
        # ToDo:
        return "", 500, {'Content-Type': 'text/plain'}

    data["sensor_api_id"] = api_credentials.get("id")
    data["sensor_api_key"] = api_credentials.get("key")

    return "Registered", 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route("/action/restart")
def actionRestart():
    return "reboot", 500, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route("/action/save")
def actionSave():
    return "Config saved to eeprom", 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route("/config/api/hostname", methods=["GET", "POST"])
def handleAPIHostname():
    if request.method == "GET":
        return data["api_hostname"], 200, {'Content-Type': 'text/plain'}

    if "hostname" not in request.form:
        return "No hostname given", 400, {'Content-Type': 'text/plain'}

    data["api_hostname"] = request.form["hostname"]
    return "Hostname set", 200, {'Content-Type': 'text/plain'}


@app.route("/config/api/port", methods=["GET", "POST"])
def handleAPIPort():
    if request.method == "GET":
        return str(data["api_port"]), 200, {'Content-Type': 'text/plain'}

    if "port" not in request.form:
        return "No port given", 400, {'Content-Type': 'text/plain'}

    data["api_port"] = int(request.form["port"])
    return "Port set", 200, {'Content-Type': 'text/plain'}


@app.route("/config/sensor/<int:sensor_id>", methods=["GET", "POST"])
def handleConfigSensor(sensor_id):
    if sensor_id < 0 or sensor_id > 32:
        return "Sensor with ID not available", 404, {"Content-Type": "text/plain"}

    if request.method == "GET":
        sensor_config = data["sensor_config"].get(sensor_id)
        if sensor_config is None:
            return "Config not found", 404

        return json.dumps(sensor_config), 200, {"Content-Type": "application/json"}

    if "type" not in request.form:
        return

    if "config" not in request.form:
        return

    # ToDo: more checks
    sensor_type = request.form.get("type")
    sensor_type = int(sensor_type)
    sensor_config = request.form.get("config")
    sensor_config = sensor_config.split(",")
    tmp = []
    for i in sensor_config:
        i = int(i)
        tmp.append(i)

    sensor_config = tmp

    data["sensor_config"][sensor_id] = {
        "type": sensor_type,
        "config": sensor_config
    }

    return "Success", 200, {'Content-Type': 'text/plain'}


@app.route("/config/wifi/sta/ssid", methods=["GET", "POST"])
def handleSSID():
    if request.method == "GET":
        if data["ssid"] == "":
            return "SSID not set", 404, {'Content-Type': 'text/plain'}
        return data["ssid"]

    if "ssid" not in request.form:
        return "No ssid given", 400, {'Content-Type': 'text/plain'}

    if len(request.form["ssid"]) == 0:
        return "SSID must at least be 1 character long", 400, {'Content-Type': 'text/plain'}

    data['ssid'] = request.form["ssid"]
    return "SSID set", 200, {'Content-Type': 'text/plain'}


@app.route("/config/wifi/sta/password", methods=["GET", "POST"])
def handlePassword():
    if request.method == "GET":
        return "", 200, {'Content-Type': 'text/plain; charset=utf-8'}

    if "password" not in request.form:
        return "No password given", 400, {'Content-Type': 'text/plain'}

    data['password'] = request.form["password"]
    return "Password set", 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route("/info/wifi/ssids")
def handleScanSSID():
    ssids = [
        {
            "ssid": "test",
            "crypt": "none"
        },
        {
            "ssid": "debug",
            "crypt": "wep"
        },
        {
            "ssid": "fake",
            "crypt": "wpa2"
        }
    ]

    result = ssids
    if "q" in request.args:
        result = []
        for ssid in ssids:
            if ssid["ssid"].startswith(request.args["q"]):
                result.append(ssid)

    return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route("/info/wifi/sta")
def handleSTA():
    status = {
        "connected": True,
        "ip": "192.168.1.2",
        "netmask": "255.255.255.0"
    }
    return json.dumps(status), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route("/setup", methods=["GET"])
def actionSetup():
    return app.send_static_file("index.html")


@app.route("/setup/js.js")
def actionSetupJS():
    return app.send_static_file("output.min.js")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True, port=5001)
