import RPi.GPIO as GPIO

from flask import Flask, render_template

from static import room_control
from static.room_control import gpio_mappings

app = Flask(__name__)


def get_status():
    fan = GPIO.input(gpio_mappings['fan'][1])
    m1 = GPIO.input(gpio_mappings['m1'][1])
    m2 = GPIO.input(gpio_mappings['m2'][1])
    m3 = GPIO.input(gpio_mappings['m3'][1])
    m4 = GPIO.input(gpio_mappings['m4'][1])
    n12 = GPIO.input(gpio_mappings['n12'][1])
    n3 = GPIO.input(gpio_mappings['n3'][1])

    templateData = {
        'fan': fan,
        'm1': m1,
        'm2': m2,
        'm3': m3,
        'm4': m4,
        'n12': n12,
        'n3': n3
    }
    return templateData


@app.route("/")
def index():
    templateData = get_status()
    return render_template('index.html', **templateData)


# The function below is executed when someone requests a URL with the actuator name and action in it
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    actuator = deviceName

    if action == "on":
        room_control.turn_on(actuator)
        print("ON")
    if action == "off":
        room_control.turn_off(actuator)
        print("OFF")

    templateData = get_status()
    return render_template('index.html', **templateData)


if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for k in gpio_mappings:
        GPIO.setup(gpio_mappings[k][1], GPIO.OUT)

    app.run(host='0.0.0.0', port=8080, debug=True)
