#!/usr/bin/env python3

import threading as th
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel
import signal

from lib import *


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
    leds.animate_rainbow()
    sleep(10)

timer = th.Timer(118, stop)

def main():
    ''' --- Programm for BigBot ---
        bot is placed 45deg bith bumper in the corner
    '''

    # set the console just how we want it
    set_cursor(OFF)

    # start
    timer.start()
    driveAdapter.odometry_start(theta_degrees_start=45)

    # init
    driveAdapter.setSpeed(spdstd)
    driveAdapter.on_for_distance(back(spdstd), 500)

    #drive to line
    driveAdapter.driveTillLine(ls)
    driveAdapter.on_for_distance(spdstd, 50)
    lifter.move_to(0)
    sleep(2)
    driveAdapter.turn_right(spdslow, 45)



    driveAdapter.driveTillBump(bumper)

    # collect poms
    gripper.position(40)
    driveAdapter.on_for_distance(-1*spdfast, 1300)
    gripper.close()

    for i in range(2):
        lifter.move(8)
        driveAdapter.on_for_distance(back(spdstd), 150-i*30)
        gripper.open()
        driveAdapter.on_for_distance(spdstd, 100+i*30)
        lifter.move_to(0)
        if not i:
            gripper.close()

    # get botgui
    driveAdapter.setSpeed(spdstd)
    driveAdapter.turn_right(spdstd, 90)

    driveAdapter.driveTillBump(bumper)
    driveAdapter.on_for_distance(back(spdstd), 150)
    driveAdapter.turn_right(spdstd, 90)
    driveAdapter.setSpeed(back(spdstd))

    driveAdapter.driveTillLine(ls)
    driveAdapter.on_for_distance(spdstd, 150)
    driveAdapter.turn_right(spdslow, 90)

    lifter.move(48)
    driveAdapter.on_for_distance(back(spdstd), 120)
    gripper.position(80)
    driveAdapter.on_for_distance(spdstd, 100)

    driveAdapter.turn_right(spdslow,90)
    driveAdapter.on_for_distance(back(spdstd), 200)
    lifter.move_to(10)
    driveAdapter.turn_right(spdstd, 25)
    driveAdapter.on_for_distance(back(spdstd), 450)

    lifter.move_to(3.6)
    gripper.open()
    driveAdapter.turn_right()
    driveAdapter.on_for_distance(spdstd, 300)
    driveAdapter.stop()
    driveAdapter.odometry_stop()


if __name__ == '__main__':
    main()
