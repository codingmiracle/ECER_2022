#!/usr/bin/env python3

import os
import sys
import time
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors

# state constants
ON = True
OFF = False


def debug_print(*args, **kwargs):
    # prints to stderr - messages show up in vscode Output
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    print('\x1Bc', end='')


def set_cursor(state):
    # set cursor True/False
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):

    os.system('setfont ' + name)


def main():
    '''The main function of our program'''

    # set the console just how we want it
    set_cursor(OFF)

    ts = ev3sensors.TouchSensor(ev3inputs.INPUT_1)
    leds = ev3leds.Leds()

    print("Press the touch sensor to change the LED color!")

    ml = ev3motors.LargeMotor(ev3motors.OUTPUT_B)
    mr = ev3motors.LargeMotor(ev3motors.OUTPUT_C)
    ma = ev3motors.MediumMotor(ev3motors.OUTPUT_A)
    ml.stop_action = ml.STOP_ACTION_BRAKE
    mr.stop_action = mr.STOP_ACTION_BRAKE
    ml.duty_cycle_sp = 50
    mr.duty_cycle_sp = 50
    while True:
        debug_print(ml.position)
        debug_print(mr.position)
        ml.run_direct()
        mr.run_direct()
        if ts.is_pressed or ml.position > 4000:
            ml.stop()
            mr.stop()
            break
    #ma.on_for_degrees(ev3motors.SpeedPercent(100), 135)
    #ma.on_for_degrees(ev3motors.SpeedPercent(100), -135)


if __name__ == '__main__':
    main()
