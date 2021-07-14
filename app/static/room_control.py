import RPi.GPIO as GPIO

import argparse
import traceback

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

general_mapping = {
    "OFF": GPIO.HIGH,
    "ON": GPIO.LOW,
}

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


def turn_off(appliance: str):
    # appliance is one of key of gpio_mapping. so m1, fan, n12 etc
    GPIO.setup(gpio_mappings[appliance][1], GPIO.OUT)
    GPIO.output(gpio_mappings[appliance][1], general_mapping['OFF'])
    print(f'{gpio_mappings[appliance][0]} OFF')


def turn_on(appliance: str):
    GPIO.setup(gpio_mappings[appliance][1], GPIO.OUT)
    GPIO.output(gpio_mappings[appliance][1], general_mapping['ON'])
    print(f'{gpio_mappings[appliance][0]} ON')


bit_mapping = {
    '1': turn_on,
    '0': turn_off
}


def fan_control(fan_args: str):
    # fan_args will be 0 or 1
    bit_mapping[fan_args]('fan')


def main_light_control(main_light_args: list):
    # main_light_args will be like ['40', '11']
    # x will be 40 or 41 or 11 etc
    for x in main_light_args:
        x_args = x[-1]  # last char tells on or off
        x_name = 'm' + x[0]  # first char tells light's name
        bit_mapping[x_args](x_name)


def night_light_control(night_light_args: list):
    # x will be 120 or 121 or 30 or 31
    for x in night_light_args:
        x_args = x[-1]  # last char tells on or off
        x_name = 'n' + x[:-1]  # before last char tells light's name
        bit_mapping[x_args](x_name)


def all_off():
    for k in gpio_mappings:
        if k.startswith('m'):
            turn_off(k)
        if k == 'fan':
            turn_off('fan')


def all_on():
    for k in gpio_mappings:
        if k.startswith('m'):
            turn_on(k)
        if k == 'fan':
            turn_on('fan')


def all_control(all_args: str):
    if int(all_args) == 1:
        all_on()
    else:
        all_off()


def person_zero():
    # all_off()
    print("last person OUT, so All off")


def person_one():
    # all_on()
    print("first person IN, so All on")


def room_control():
    parser = argparse.ArgumentParser(description='Room Control')
    parser.add_argument('-f', '--fan', type=str, choices=['0', '1'],
                        help="0 : fan off, 1 : fan on")
    parser.add_argument('-m', '--main_light', type=str, nargs='*',
                        choices=['10', '11', '20', '21', '30', '31', '40', '41'],
                        help="x0 : main light x off, x1 : main light x on. For all x E [1, 4]"
                             "\nMultiple agrs supported")
    parser.add_argument('-n', '--night_light', type=str, nargs='*',
                        choices=['120', '121', '30', '31'],
                        help="x0 : night light x off, x1 : night light x on. For all x E {12, 3}"
                             "\nMultiple agrs supported")
    parser.add_argument('-a', '--all', type=str, choices=['0', '1'],
                        help="0 : all main lights & fan off, 1 : all main lights & fan on")

    # Parse and print the results
    args = parser.parse_args()

    try:
        if args.all:
            all_control(args.all)

        if args.main_light:
            main_light_control(args.main_light)

        if args.fan:
            fan_control(args.fan)

        if args.night_light:
            night_light_control(args.night_light)

    except:
        print("Some error occurred! \n")
        print(traceback.print_exc())

        # todo: below is not working on error (its not turning off everything)
        GPIO.cleanup()
    else:
        print("All Went Well!")


if __name__ == "__main__":
    room_control()
    # todo: add timer functionality and ability to switch on and off at specific time
