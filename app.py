import os
import Switch
from flask import Flask, render_template, request
import logging

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

Switch_list = [
    [Switch.Switch(1, 1, "LED Schreibtisch", '7145473', '7145475'),
     Switch.Switch(1, 2, "Ecklampe", "1361", "1364"),
     Switch.Switch(1, 3, "Tischlampe", "4433", "4436")],
    [Switch.Switch(2, 4, "Stehlampe", '11742167 4 355', '11559223 4 355'),
     Switch.Switch(2, 5, "Leuchtkugel", '11940012 4 355', '12494204 4 355'),
     Switch.Switch(2, 6, "Deckenfluter", '12494206 4 355', '11940014 4 355'),
     Switch.Switch(2, 7, "Alles", '11735922 4 355', '12052066 4 355', True)]
]


def find_switch(key):
    for group_list in Switch_list:
        for e in group_list:
            if str(e.num) == key:
                return e
    return None


def rf_sender(code):
    # dev
    # print("DEBUG: CODE SEND: " + code)
    os.system("./codesend " + code)
    os.system("./codesend " + code)  # to make sure it worked


def multi_switch_switcher(multi_switch, value):
    """
    Some switches (RF codes) control several devices. Changes Status of all group devices to account for that.
    :param value: value of command (OFF;ON)
    :param multi_switch: MultiSwitches which control several devices
    """
    for group_list in Switch_list:
        for switch in group_list:
            if switch.group == multi_switch.group:
                if value == "ON":
                    switch.enabled = True
                elif value == "OFF":
                    switch.enabled = False


def kill_switch():
    for group_list in Switch_list:
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
            switch.enabled = False
            rf_sender(switch.code_off)


def switcher(request_dic):
    for key, value in request_dic.items():
        if value == "KILL":
            kill_switch()
            return
        switch = find_switch(key)
        if value == "ON":
            if switch.is_multi_switch:
                multi_switch_switcher(switch, value)
            switch.enabled = True
            app.logger.info(f'{switch.num}: {switch.name}: turned on')
            #  print(f'{switch.num}: {switch.name}: turned on')
            rf_sender(switch.code_on)
        elif value == "OFF":
            if switch.is_multi_switch:
                multi_switch_switcher(switch, value)
            switch.enabled = False
            app.logger.info(f'{switch.num}: {switch.name}: turned off')
            # print(f'{switch.num}: {switch.name}: turned off')
            rf_sender(switch.code_off)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        request_dic = request.form.to_dict()
        app.logger.info("Request: " + str(request.form.to_dict()))
        if len(request_dic) <= 0:
            pass
        else:
            switcher(request_dic)

    elif request.method == 'GET':
        return render_template("index.html", switches=Switch_list, form=request.form)

    return render_template("index.html", switches=Switch_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
