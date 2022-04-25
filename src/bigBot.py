#!/usr/bin/env python3

import threading as th
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
leds = ev3leds.Leds()
ls = ev3sensors.ColorSensor(ev3inputs.INPUT_1)
bumper = Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3)

driveAdapter = DriveAdapter(OUTPUT_B, OUTPUT_D, ev3dev2.wheel.EV3Tire, 93, True)
gripper = Gripper(ev3motors.OUTPUT_A)
lifter = Lifter(ev3motors.OUTPUT_C)
driveAdapter.cs = ls

def stop():
    debug_print("Time is up!")
    driveAdapter.stop()
    gripper.stop()
    lifter.stop()
    while True:
        leds.animate_stop()

timer = th.Timer(118, stop)

def main():
    ''' --- Programm for BigBot --- '''

    # set the console just how we want it
    set_cursor(OFF)

    #waitTillLights(ON, ls)
    timer.start()

    driveAdapter.odometry_start(theta_degrees_start=45)
    # align back -> bad for odometry
    # while True:
    #     driveAdapter.on(SpeedRPM(-50), SpeedRPM(-50))
    #     if bumper.pressed_front():
    #         driveAdapter.stop()
    #         break

    # init
    # driveAdapter.turn_right(spdstd, 135)
    # lifter.move_absolut(0)

    driveAdapter.driveTillLine(ls)
    driveAdapter.on_for_distance(spdstd, 170)

    driveAdapter.turn_left(spdslow, 90)
    #align back
    while True:
        driveAdapter.on(spdstd, spdstd)
        if bumper.pressed_front():
            sleep(0.2)
            driveAdapter.stop()
            break

    gripper.position(20)
    driveAdapter.setSpeed(-1*spdfast)
    driveAdapter.driveTillLine(ls)

    driveAdapter.on_for_seconds(SpeedRPM(-60), SpeedRPM(-40), 0.5)
    driveAdapter.on_for_distance(-1*spdfast, 700)
    gripper.close()


    driveAdapter.stop()
    driveAdapter.odometry_stop()




if __name__ == '__main__':
    main()
