#!/usr/bin/env python3

import unittest
import threading as th
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel

from lib import *


class Test(unittest.TestProgram):
    def __init__(self) -> None:
        self.attributes = "place here"
        self.bumper = Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3)
        self.leds = ev3leds.Leds()
        self.driveAdapter =  DriveAdapter(OUTPUT_B, OUTPUT_D, ev3dev2.wheel.EV3Tire, 93, True)
        self.gripper = Gripper(ev3motors.OUTPUT_A)
        self.lifter = Lifter(ev3motors.OUTPUT_C)
        self.ls = ev3sensors.ColorSensor(ev3inputs.INPUT_1)

    def run(self):
        bb_main()

        # self.lifter.height = 0
        # self.lifter.move(50)
        # self.driveAdapter.on_for_distance(back(spdstd), 100)
        # self.gripper.position(80)
        # self.driveAdapter.on_for_distance(spdstd, 200)
        # self.lifter.move_to(0)
        # self.driveAdapter.turn_left(spdslow, 180)




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

def bb_main():
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
    lifter.move_to(0)
    driveAdapter.on_for_distance(spdstd, 20)
    sleep(0.4)
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
    # drive s shape back and drive till Line
    driveAdapter.on(spdfast, spdslow)
    sleep(0.5)
    driveAdapter.on(spdstd, spdfast)
    sleep(1)
    driveAdapter.stop()
    driveAdapter.driveTillLine(ls)
    driveAdapter.on_for_distance(spdstd, 150)
    driveAdapter.turn_left(spdslow, 90)

    lifter.move(52)
    driveAdapter.on_for_distance(back(spdstd), 150)
    gripper.position(80)
    driveAdapter.on_for_distance(spdstd, 200)
    lifter.move_to(10)
    driveAdapter.on_for_distance(spdstd, 600)

    lifter.move_to(3.6)
    gripper.open()
    driveAdapter.stop()
    driveAdapter.odometry_stop()




if __name__ == '__main__':
    t = Test()
    t.run()





# get botguy code von test.run()
        # self.lifter.move_to(0)
        # self.driveAdapter.on_for_distance(back(spdfast), 300)
        # self.driveAdapter.turn_right(spdstd, 135)
        # self.driveAdapter.setSpeed(spdfast)
        # self.driveAdapter.driveTillBump(Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3))
        # self.driveAdapter.on_for_distance(back(spdstd), 100)
        # self.driveAdapter.turn_right(spdstd, 90)
        # self.driveAdapter.driveTillLine(self.ls)
        # self.driveAdapter.on_for_distance(spdstd, 150)
        # self.driveAdapter.turn_right(spdstd, 90)
        # self.lifter.move_to(50)
        # self.driveAdapter.on_for_distance(back(spdstd), 100)
        # self.gripper.close()
