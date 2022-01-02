import os
import Switch
from flask import Flask, render_template, request
import logging

app = Flask(__name__)
# https://forum.pimatic.org/topic/3337/433-mhz-funksteckdosen-lidl-silvercrest-rcr-dp3-3711-a-brennenstuhl-mit-homeduino
# A     11940012        12494204
# B     11704053        11742165
# C     12494206        11940014
# D     11742167        11559223
# codes for the home funksender
app.logger.setLevel(logging.INFO)

Switch_list = [
    Switch.Switch(1, "LED Schreibtisch", '7145473', '7145475'),
    Switch.Switch(2, "Stehlampe", '11742167 4 355', '11559223 4 355'),
    Switch.Switch(3, "Leuchtkugel", '11940012 4 355', '12494204 4 355'),
    Switch.Switch(4, "Deckenfluter", '12494206 4 355', '11940014 4 355'),
    Switch.Switch(5, "Alles", '11735922 4 355', '12052066 4 355')
]


def find_switch(key):
    for e in Switch_list:
        if str(e.num) == key:
            return e
    return None


def rf_sender(code):
    # dev
    #print("DEBUG: CODE SEND: " + code)
    os.system("./codesend " + code)
    os.system("./codesend " + code)  # to make sure it worked


def multiSwitchSwitcher(switch, value):
    """
    Some switches (RF codes) control several devices. Changen Status of Hardcoded devices to account for that.
    :param value: value of command (OFF;ON)
    :param switch: MultiSwitches which control several devices
    """
    if value == "ON":
        if switch.num == 5:
            Switch_list[1].enabled = True
            Switch_list[2].enabled = True
            Switch_list[3].enabled = True
            Switch_list[4].enabled = True
    elif value == "OFF":
        if switch.num == 5:
            Switch_list[1].enabled = False
            Switch_list[4].enabled = False
            Switch_list[3].enabled = False
            Switch_list[2].enabled = False




@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        request_dic = request.form.to_dict()
        app.logger.info("Request: " + str(request.form.to_dict()))
        if len(request_dic) <= 0:
            pass
        else:
            for key, value in request_dic.items():
                switch = find_switch(key)
                if value == "ON":
                    multiSwitchSwitcher(switch, value)  # used to switch several devices TODO fix hardcode
                    switch.enabled = True
                    app.logger.info(f'{switch.num}: {switch.name}: turned on')

                    #  print(f'{switch.num}: {switch.name}: turned on')
                    rf_sender(switch.code_on)
                elif value == "OFF":
                    multiSwitchSwitcher(switch, value)
                    switch.enabled = False
                    app.logger.info(f'{switch.num}: {switch.name}: turned off')
                    # print(f'{switch.num}: {switch.name}: turned off')
                    rf_sender(switch.code_off)

    elif request.method == 'GET':
        return render_template("index.html", switches=Switch_list, form=request.form)

    return render_template("index.html", switches=Switch_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
