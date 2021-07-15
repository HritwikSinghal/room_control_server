import os

DEBUG = int(os.getenv("MY_DEBUG"))

if not DEBUG:
    import RPi.GPIO as GPIO
    from app.static import room_control
    from app.static.room_control import gpio_mappings
else:
    gpio_mappings = {
        'm1': ['Main Light 1', 2],
        'm2': ['Main Light 2', 3],
        'm3': ['Main Light 3', 4],
        'm4': ['Main Light 4', 14],

        'n12': ['Night Light 1 & 2', 15],
        'n3': ['Night Light 3', 18],

        'fan': ['Fan', 17],
        'extra': ['Extra', 27],
    }

from flask import Flask, render_template, redirect, request
from werkzeug.useragents import UserAgent

app = Flask(__name__)

input_mapping = {
    0: "On",
    1: "Off"
}


def get_status():
    if not DEBUG:
        # if fan is : 0 == ON, 1 == OFF
        fan = GPIO.input(gpio_mappings['fan'][1])
        m1 = GPIO.input(gpio_mappings['m1'][1])
        m2 = GPIO.input(gpio_mappings['m2'][1])
        m3 = GPIO.input(gpio_mappings['m3'][1])
        m4 = GPIO.input(gpio_mappings['m4'][1])
        n12 = GPIO.input(gpio_mappings['n12'][1])
        n3 = GPIO.input(gpio_mappings['n3'][1])

        templateData = {
            'fan': [fan, input_mapping[fan]],
            'm1': [m1, input_mapping[m1]],
            'm2': [m2, input_mapping[m2]],
            'm3': [m3, input_mapping[m3]],
            'm4': [m4, input_mapping[m4]],
            'n12': [n12, input_mapping[n12]],
            'n3': [n3, input_mapping[n3]]
        }
    else:

        templateData = {
            'fan': [0, 'Off'],
            'm1': [1, 'Off'],
            'm2': [0, 'Off'],
            'm3': [1, 'Off'],
            'm4': [0, 'Off'],
            'n12': [1, 'Off'],
            'n3': [0, 'Off']
        }

    return templateData


@app.route("/")
def index():
    user_agent = UserAgent(request.headers.get('User-Agent')).browser
    print(f'user_agent = {user_agent}')

    if ("firefox" in user_agent or 'safari' in user_agent) and ('chrome' not in user_agent):
        templateData = get_status()
        return render_template('index.html', **templateData)
    else:
        return "Some Error Occurred! Please contact Administrator."


# The function below is executed when someone requests a URL with the actuator name and action in it
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'all':
        if action == 'on':
            room_control.all_on()
        if action == 'off':
            room_control.all_off()

    else:
        if action == "on":
            room_control.turn_on(deviceName)
            print(f"{deviceName} ON")
        if action == "off":
            room_control.turn_off(deviceName)
            print(f"{deviceName} OFF")

    return redirect('/')


@app.route('/old')
def old_int():
    user_agent = UserAgent(request.headers.get('User-Agent')).browser
    print(f'user_agent = {user_agent}')

    if ("firefox" in user_agent or 'safari' in user_agent) and ('chrome' not in user_agent):
        templateData = get_status()
        return render_template('old_int.html', **templateData)

    else:
        return "Some Error Occurred! Please contact Administrator."


def start():
    if not DEBUG:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for k in gpio_mappings:
            GPIO.setup(gpio_mappings[k][1], GPIO.OUT)

    app.run(host='0.0.0.0', port=8080, debug=bool(DEBUG))
