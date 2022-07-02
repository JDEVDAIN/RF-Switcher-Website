import json
from flask import Flask, render_template, request
import logging
import subprocess
from Switches import SWITCH_LIST

app = Flask(__name__)
# https://forum.pimatic.org/topic/3337/433-mhz-funksteckdosen-lidl-silvercrest-rcr-dp3-3711-a-brennenstuhl-mit-homeduino
# codes for the home funksender
# A     11940012        12494204
# B     11704053        11742165
# C     12494206        11940014
# D     11742167        11559223

# codes for brennstuhl
# A 1361 1364
# B 4433 4436
# C 5201 5204
app.logger.setLevel(logging.INFO)


def find_switch(key):
    for group_list in SWITCH_LIST:
        for e in group_list:
            if str(e.num) == key:
                return e
    return None


def rf_sender(code):
    # dev
    #print("DEBUG: CODE SEND: " + code)
    args_list = ["./codesend"]
    args_list.extend(code.split())
    subprocess.call(args_list)


def multi_switch_switcher(multi_switch, value):
    """
    Some switches (RF codes) control several devices. Changes Status of all group devices to account for that.
    :param value: value of command (OFF;ON)
    :param multi_switch: MultiSwitches which control several devices
    """
    for group_list in SWITCH_LIST:
        if multi_switch in group_list:
            for switch in group_list:
                if value == "ON":
                    switch.enabled = True
                elif value == "OFF":
                    switch.enabled = False


def kill_switch():
    for group_list in SWITCH_LIST:
        # find multi switch and activate to deactivate group instead of disabling all
        # could be speed up; This iteration could be skipped if all multiswitches will get set at the end of a group
        # depending on the hardware
        for switch in group_list:
            if switch.is_multi_switch:
                multi_switch_switcher(switch, "OFF")
                app.logger.info(f'{switch.num}: {switch.name}: turned off')
                rf_sender(switch.code_off)
                return
        for switch in group_list:
            app.logger.info(f'{switch.num}: {switch.name}: turned off')
            if switch.enabled:
                switch.enabled = False
                rf_sender(switch.code_off)


def switcher(switchName, switchValue):
    if switchValue == "KILL":
        kill_switch()
        return
    switch = find_switch(switchName)
    if switchValue == "ON":
        if switch.is_multi_switch:
            multi_switch_switcher(switch, switchValue)
        switch.enabled = True
        app.logger.info(f'{switch.num}: {switch.name}: turned on')
        #  print(f'{switch.num}: {switch.name}: turned on')
        rf_sender(switch.code_on)
    elif switchValue == "OFF":
        if switch.is_multi_switch:
            multi_switch_switcher(switch, switchValue)
        switch.enabled = False
        app.logger.info(f'{switch.num}: {switch.name}: turned off')
        # print(f'{switch.num}: {switch.name}: turned off')
        rf_sender(switch.code_off)


@app.route("/api/switches", methods=['POST'])
def switcherApi():
    if request.method == 'POST':  # maybe make two endpoints
        if request.is_json:
            changed_switch = request.get_json()

            switcher(changed_switch["name"], changed_switch["value"])
            flat_switch_list = [switch for group_list in SWITCH_LIST for switch in group_list]
            json_switch_list = [switch.toSimpleJSON() for switch in flat_switch_list]

            return json.dumps({"switch_list": json_switch_list}, default=vars), 200, {'ContentType': 'application/json'}


@app.route("/api/status/<string:switch_num>", methods=['GET'])
def statusApi(switch_num):
    selected_switch = find_switch(switch_num)
    is_switch_enabled = find_switch(switch_num).enabled
    # To make sure the light is always synced with the switch, send a rf request to be on the safe site
    switcher(switch_num, "ON" if is_switch_enabled else "OFF")
    return json.dumps({"status": "ON" if is_switch_enabled else "OFF"})

@app.route("/")
def index():
    if request.method == 'GET':
        return render_template("index.html", switches=SWITCH_LIST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
