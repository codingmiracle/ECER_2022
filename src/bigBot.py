#!/usr/bin/env python3

from logging import raiseExceptions
import os
import sys
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel
import signal

from lib import *

# --- Functions ---

def timeout_handler(signal, frame):
    raise Exception('Time is up!')
signal.signal(signal.SIGALRM, timeout_handler)

# --- Motors and Sensors here ---

ls = ev3sensors.ColorSensor(ev3inputs.INPUT_1)
bumper = Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3)

driveAdapter = DriveAdapter(OUTPUT_B, OUTPUT_C, ev3dev2.wheel.EV3Tire, 108)
gripper = Gripper(ev3motors.OUTPUT_A)
#ropeMotor = ev3motors.MediumMotor(ev3motors.OUTPUT_D)
driveAdapter.cs = ls


def main():
    ''' --- Programm for BigBot --- '''

    # set the console just how we want it
    set_cursor(OFF)

    #waitTillLightsOff

    signal.alarm(118)

    try:


        # align back -> bad for odometry
        # while True:
        #     driveAdapter.on(SpeedRPM(-50), SpeedRPM(-50))
        #     if bumper.pressed_front():
        #         driveAdapter.stop()
        #         break

        driveAdapter.odometry_start(theta_degrees_start=45)

        driveAdapter.on_for_distance(SpeedRPM(50), 200)


        driveAdapter.odometry_stop()

    except:
        #stop everything
        debug_print("Time is up!")
        driveAdapter.stop()



if __name__ == '__main__':
    main()
