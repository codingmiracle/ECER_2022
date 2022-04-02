#!/usr/bin/env python3

import os
import sys
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel

from drive import *

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

    bumper = Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3)
    driveAdapter = MoveDifferential(OUTPUT_B, OUTPUT_C, ev3dev2.wheel.EV3Tire, 108)
    driveAdapter.odometry_start()

    driveAdapter.on_to_coordinates(SpeedRPM(80), 300, 300)




    driveAdapter.odometry_stop()


if __name__ == '__main__':
    main()
