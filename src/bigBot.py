#!/usr/bin/env python3

import os
import sys
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel

from lib import *

# --- Functions ---



def main():
    ''' --- Programm for BigBot --- '''

    # set the console just how we want it
    set_cursor(OFF)

    ls = ev3sensors.ColorSensor(ev3inputs.INPUT_1)
    bumper = Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3)

    driveAdapter = MoveDifferential(OUTPUT_B, OUTPUT_C, ev3dev2.wheel.EV3Tire, 108)
    driveAdapter.cs = ls

    # align back
    while True:
        driveAdapter.on(SpeedRPM(-50), SpeedRPM(-50))
        if bumper.pressed_front():
            driveAdapter.stop()
            break

    driveAdapter.odometry_start(theta_degrees_start=45)

    # --- until here works as expected ---

    driveAdapter.on_for_degrees(SpeedRPM(80), SpeedRPM(80), 90)
    driveAdapter.on_to_coordinates(SpeedRPM(80), 600, 200)


    # while True:
    #     if ls.reflected_light_intensity > 80:
    #         driveAdapter.on(SpeedRPM(70), SpeedRPM(100))
    #     elif ls.reflected_light_intensity < 20:
    #         driveAdapter.on(SpeedRPM(100), SpeedRPM(70))

    driveAdapter.odometry_stop()


if __name__ == '__main__':
    main()
