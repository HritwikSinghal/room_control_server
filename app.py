import RPi.GPIO as GPIO
from flask import Flask, render_template, redirect, request

from werkzeug.useragents import UserAgent

from static import room_control
from static.room_control import gpio_mappings

app = Flask(__name__)

input_mapping = {
    0: "On",
    1: "Off"
}


def get_status():
    # 0 == ON, 1 == OFF
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


if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for k in gpio_mappings:
        GPIO.setup(gpio_mappings[k][1], GPIO.OUT)

    app.run(host='0.0.0.0', port=8080, debug=True)
