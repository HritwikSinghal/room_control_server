import signal
import sys
import threading
import time
import traceback
import room_control

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

general_mapping = {
    "OFF": GPIO.HIGH,
    "ON": GPIO.LOW,
}

gpio_mappings = {
    'ir_in': ['ir_in', 10],
    'ir_out': ['ir_out', 21],
}


def ir_in_control():
    global in_ir_updated, room_in_ir_time

    in_pin = gpio_mappings['ir_in'][1]
    GPIO.setup(in_pin, GPIO.IN)

    while True:
        val = int(GPIO.input(in_pin))
        if val == 1:
            room_in_ir_time = time.time()
            in_ir_updated = 1
            print("IN", val, time.time())
            threading.Event().wait(0.5)


def ir_out_control():
    global room_out_ir_time, out_ir_updated
    out_pin = gpio_mappings['ir_out'][1]
    GPIO.setup(out_pin, GPIO.IN)

    while True:
        val = int(GPIO.input(out_pin))
        if val == 1:
            room_out_ir_time = time.time()
            out_ir_updated = 1
            print("OUT", val, time.time())
            threading.Event().wait(0.5)


if __name__ == "__main__":
    try:

        total_person = 0
        room_in_ir_time = -1
        room_out_ir_time = -1

        in_ir_updated = 0
        out_ir_updated = 0

        # creating thread
        t1 = threading.Thread(target=ir_in_control)
        t2 = threading.Thread(target=ir_out_control)

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()

        while True:
            try:
                if in_ir_updated == 1 and out_ir_updated == 0:
                    print("# person moving out and is between in and out sensor")
                    # person moving out and is between in and out sensor
                    threading.Event().wait(1)

                    if out_ir_updated == 0:
                        # false alarm
                        in_ir_updated = 0
                        out_ir_updated = 0
                        print("false alarm")
                        continue

                    elif room_out_ir_time - room_in_ir_time < 2:
                        # person moved out
                        in_ir_updated = 0
                        out_ir_updated = 0

                        room_in_ir_time = -1
                        room_out_ir_time = -1

                        if total_person == 1:
                            room_control.person_zero()
                        total_person = max(0, total_person - 1)
                        print("Someone went out of room, Relax!")
                        print("Total person", total_person, end='\n\n')

                    else:
                        print("some error in Moving out code, error code : 1")

                elif out_ir_updated == 1 and in_ir_updated == 0:
                    print("# person coming in and in between out and in sensor")
                    # person coming in and in between out and in sensor
                    threading.Event().wait(1)

                    if in_ir_updated == 0:
                        # false alarm
                        in_ir_updated = 0
                        out_ir_updated = 0
                        print("false alarm")
                        continue

                    elif room_in_ir_time - room_out_ir_time < 2:
                        # person came in
                        in_ir_updated = 0
                        out_ir_updated = 0

                        room_in_ir_time = -1
                        room_out_ir_time = -1
                        if total_person == 0:
                            room_control.person_one()
                        total_person = min(15, total_person + 1)
                        print("Someone came in room, Beware!")
                        print("Total person", total_person, end='\n\n')
            except:
                traceback.print_exc()
                in_ir_updated = 0
                out_ir_updated = 0
                print("New Try except block")
                signal.signal(signal.SIGINT, exit(0))
                continue

    except:
        print("There was some error in threading! \n")
        traceback.print_exc()
        sys.exit(0)
        # GPIO.cleanup()
