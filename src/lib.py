#!/usr/bin/env python3


from ev3dev2.motor import *
from ev3dev2.led import *

from ev3dev2.sensor.lego import *
from ev3dev2.sensor import *

import time

#------------------
# debuging functions
#------------------
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


#------------------
# our own DriveAdapter
#------------------
spdslow = SpeedRPM(20)
spdstd = SpeedRPM(50)
spdfast = SpeedRPM(80)
class DriveAdapter(MoveDifferential):

    def __init__(self, left, right, wheel_class, wheel_dist, inversed) -> None:
        super().__init__(left, right, wheel_class, wheel_dist)
        super().odometry_start()
        super().odometry_coordinates_log()
        if inversed:
            super().right_motor.polarity = 'inversed'
            super().left_motor.polarity = 'inversed'

    def followLineBackForms(self, cs, ms, startsright=True):
        starttime = time.time()
        isright = startsright
        while time.time() < starttime + ms/1000:
            if isright:
                while cs.reflected_light_intensity > 25:
                    super().on(SpeedRPM(60), SpeedRPM(60))
                while cs.reflected_light_intensity < 25:
                    super().on(SpeedRPM(60), SpeedRPM(30))
                isright = False
            else:
                while cs.reflected_light_intensity > 25:
                    super().on(SpeedRPM(60), SpeedRPM(60))
                while cs.reflected_light_intensity < 25:
                    super().on(SpeedRPM(30), SpeedRPM(60))
                isright = True
        super().stop()
        if isright:
            super().turn_left(SpeedRPM(40), 12)
        else:
            super().turn_right(SpeedRPM(40), 12)

    def driveTillLineBack(self, cs):
        while cs.reflected_light_intensity > 25:
            super().on(SpeedRPM(-60), SpeedRPM(-60))
        super().stop()

    def driveTillFloorBack(self, cs):
        while cs.reflected_light_intensity < 25:
            super().on(SpeedRPM(-60), SpeedRPM(-60))
        super().stop()

# pure functions:
def followLineBackForms(driveAdapter, cs, ms, startsright=True):
    starttime = time.time()
    isright = startsright
    while time.time() < starttime + ms/1000:
        if isright:
            while cs.reflected_light_intensity > 25:
                driveAdapter.on(SpeedRPM(-60), SpeedRPM(-60))
            while cs.reflected_light_intensity < 25:
                driveAdapter.on(SpeedRPM(-60), SpeedRPM(-30))
            isright = False
        else:
            while cs.reflected_light_intensity > 25:
                driveAdapter.on(SpeedRPM(-60), SpeedRPM(-60))
            while cs.reflected_light_intensity < 25:
                driveAdapter.on(SpeedRPM(-30), SpeedRPM(-60))
            isright = True
    driveAdapter.stop()
    if isright:
        driveAdapter.turn_left(SpeedRPM(40), 12)
    else:
        driveAdapter.turn_right(SpeedRPM(40), 12)

def driveTillLineBack(driveAdapter, cs):
    while cs.reflected_light_intensity > 25:
        driveAdapter.on(SpeedRPM(-60), SpeedRPM(-60))
    driveAdapter.stop()

def driveTillFloorBack(driveAdapter, cs):
    while cs.reflected_light_intensity < 25:
        driveAdapter.on(SpeedRPM(-60), SpeedRPM(-60))
    driveAdapter.stop()


#------------------
# Bumper class
#------------------

class Bumper:
    def __init__(self,inLeft, inRight) -> None:
        self.tsl = TouchSensor(inLeft)
        self.tsr = TouchSensor(inRight)
        self.laststate = 0

    def pressed_front(self):
        if self.tsl.is_pressed and self.tsr.is_pressed:
            self.laststate = 1
            return True
        return False

    def pressed_right(self):
        if not self.tsl.is_pressed and self.tsr.is_pressed:
            self.laststate = 3
            return True
        return False

    def pressed_left(self):
        if self.tsl.is_pressed and  not self.tsr.is_pressed:
            self.laststate = 2
            return True
        return False

    def realesed(self):
        if self.laststate > 0 and not self.tsl.is_pressed and not self.tsr.is_pressed:
            self.laststate = 0
            return True
        return False

# def move_lift(cm,port): -> to class
#     lift_motor = ev3dev2.motor.MediumMotor(port)

#     rotations = cm/3

#     lift_motor.on_for_rotations(100,rotations)


#------------------
# Gripper Class
#------------------
class Gripper(MediumMotor):
    def __init__(self, Port) -> None:
        super().__init__(Port)
        self.degrees = 0 # 0 = closed, 360 = open

    def open(self):
        super().on_for_degrees(SpeedRPM(40), 360-self.degrees)
        self.degrees = 360

    def close(self):
        super().on_for_degrees(SpeedRPM(-40), self.degrees)
        self.degrees = 0

    def position(self, percent):
        super().on_for_degrees(SpeedRPM(40), (percent * 3.6)-self.degrees)
        self.degrees = percent*3.6
