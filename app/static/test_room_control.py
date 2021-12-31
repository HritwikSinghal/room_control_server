import threading
import time
import traceback

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

general_mapping = {
    "OFF": GPIO.HIGH,
    "ON": GPIO.LOW,
}

# make these dynamic
gpio_mappings = {
    'ml1': 2,
    'ml2': 3,
    'ml3': 4,
    'ml4': 14,

    'nl12': 15,
    'nl3': 18,

    'fan': 17,
    'extra': 27,

    'ir_in': 11,
    'ir_out': 26,

}


def test_ir_control():
    ir_pin = [25]

    GPIO.setup(ir_pin[0], GPIO.IN)
    while True:
        val = GPIO.input(ir_pin[0])
        print(val)
        time.sleep(0.1)


def test_relay_control():
    relays = [
        2, 3, 4,
        14, 15, 18,
        17, 27
    ]

    for relay in relays:
        GPIO.setup(relay, GPIO.OUT)
        GPIO.output(relay, GPIO.HIGH)

    try:
        while True:
            for relay in relays:
                GPIO.output(relay, GPIO.LOW)
                print(f"Relay {relay} ON")
                time.sleep(1)

            print()

            for relay in relays:
                GPIO.output(relay, GPIO.HIGH)
                print(f"Relay {relay} OFF")
                time.sleep(1)

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    try:
        # creating thread
        t1 = threading.Thread(target=test_relay_control)
        t2 = threading.Thread(target=test_ir_control)

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()

        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()

    except:
        print("There was some error in threading! \n")
        traceback.print_exc()

        GPIO.cleanup()
