#!/usr/bin/env python3

#------------------
# useless so far!!!
#------------------


from ev3dev2.motor import *
from ev3dev2.led import *

from ev3dev2.sensor.lego import *
import ev3dev2.sensor as sensor


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

