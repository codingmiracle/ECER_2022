#!/usr/bin/env python3

import unittest
import threading as th
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel

from lib import *

# --- Functions ---

def print_pass(test_name):
    print(f"{test_name}:\t Pass ✅", file=sys.stderr)
def print_fail(test_name):
    print(f"{test_name}:\t Fail ❌", file=sys.stderr)

def test(func):
    try:
        func()
        print_pass(func.__name__)
    except:
        print_fail(func.__name__)

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
        set_cursor(OFF)
        # get botguy
        # self.lifter.move_absolut(0)
        # self.driveAdapter.on_for_distance(back(spdfast), 300)
        # self.driveAdapter.turn_right(spdstd, 135)
        # self.driveAdapter.setSpeed(spdfast)
        # self.driveAdapter.driveTillBump(Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3))
        # self.driveAdapter.on_for_distance(back(spdstd), 100)
        # self.driveAdapter.turn_right(spdstd, 90)
        # self.driveAdapter.driveTillLine(self.ls)
        # self.driveAdapter.on_for_distance(spdstd, 150)
        # self.driveAdapter.turn_right(spdstd, 90)
        # self.lifter.move_absolut(50)
        # self.driveAdapter.on_for_distance(back(spdstd), 100)
        # self.gripper.close()
        self.lifter.set_height(20)
        self.lifter.move_absolut(0)
        self.lifter.move_absolut(53)




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

    # waitTillLights(ON, ls)
    timer.start()

    driveAdapter.odometry_start(theta_degrees_start=45)

    # align back -> bad for odometry
    # while True:
    #     driveAdapter.on(SpeedRPM(-50), SpeedRPM(-50))
    #     if bumper.pressed_front():
    #         driveAdapter.stop()
    #         break

    # init
    lifter.move_absolut(20)
    driveAdapter.turn_right(spdstd, 135)
    #lifter.move_absolut(0)
    lifter.set_height(0)

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
    lifter.move_absolut(0)
    gripper.position(20)
    driveAdapter.setSpeed(-1*spdfast)
    driveAdapter.driveTillLine(ls)

    driveAdapter.on_for_seconds(SpeedRPM(-60), SpeedRPM(-40), 0.5)
    driveAdapter.on_for_distance(-1*spdfast, 700)
    gripper.close()

    for i in range(2):
        lifter.move_relativ(20)
        driveAdapter.on_for_distance(back(spdstd), 100+i*30)
        gripper.open()
        driveAdapter.on_for_distance(spdstd, 100+i*30)
        lifter.move_absolut(0)
        if not i:
            gripper.close()

    driveAdapter.on_for_distance(spdstd, 50)
    driveAdapter.turn_right(spdstd, 90)




    driveAdapter.stop()
    driveAdapter.odometry_stop()




if __name__ == '__main__':
    t = Test()
    # t.run()
    # test(bb_main)
