#!/usr/bin/env python3


import signal
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel

from lib import *

# --- Functions ---

def timeout_handler(signal, frame):
    raise Exception('Time is up!')
signal.signal(signal.SIGALRM, timeout_handler)

# --- Motors and Sensors here ---

ls = ev3sensors.ColorSensor(ev3inputs.INPUT_1)

driveAdapter = MoveDifferential(OUTPUT_B, OUTPUT_D, ev3dev2.wheel.EV3Tire, 108)
driveAdapter.cs = ls

def main():
    ''' --- Programm for SmallBot --- '''

    # set the console just how we want it
    set_cursor(OFF)

    waitTillLights(ON, ls)

    signal.alarm(118)
    driveAdapter.odometry_start(theta_degrees_start=45) # 0 degrees = facing east

    try:


        # --- when driving with odometry at -45 degrees x cords are negative ---  -> get rid of coords do with on_for_distance(..., mm)

        driveAdapter.on_to_coordinates(SpeedRPM(80), 200, 0)
        driveAdapter.on_to_coordinates(SpeedRPM(80), 0, 200)


        # while True:
        #     if ls.reflected_light_intensity > 80:
        #         driveAdapter.on(SpeedRPM(70), SpeedRPM(100))
        #     elif ls.reflected_light_intensity < 20:
        #         driveAdapter.on(SpeedRPM(100), SpeedRPM(70))

        driveAdapter.odometry_stop()


    except:
        #stop everything
        debug_print("Time is up!")
        driveAdapter.stop()


if __name__ == '__main__':
    main()
