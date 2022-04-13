#!/usr/bin/env python3


from ev3dev2.motor import *
from ev3dev2.led import *

from ev3dev2.sensor.lego import *
import ev3dev2.sensor as sensor

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

class DriveAdapter(MoveDifferential):

    def __init__(self, left, right, wheel_class, wheel_dist) -> None:
        super().__init__(left, right, wheel_class, wheel_dist)
        super().odometry_start()
        super().odometry_coordinates_log()
        self.x = 0
        self.y = 0

    def on_for_distance(self, speed, distance_mm, brake=True, block=True):
        return super().on_for_distance(speed, distance_mm, brake, block)

    def on_to_coordinates(self, speed, x_target_mm, y_target_mm, brake=True, block=True):
        return super().on_to_coordinates(speed, x_target_mm, y_target_mm, brake, block)


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

