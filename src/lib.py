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

    def __init__(self, left, right, wheel_class, wheel_dist, inversed=False) -> None:
        super().__init__(left, right, wheel_class, wheel_dist)
        super().odometry_start()
        super().odometry_coordinates_log()
        self.speed = spdstd
        self.stop = 0
        if inversed:
            super().set_polarity('inversed')

    def setSpeed(self, spd=spdstd):
        self.speed = spd

    def stop(self, motors=None, brake=True):
        return super().stop(motors, brake)

    def followLineForSecs(self, cs, s):
        starttime = time.time()
        while time.time() < starttime + s:
            if self.stop:
                super().stop()
                sys.exit()
                break

            if cs.reflected_light_intensity < 25:
                super().on(SpeedRPM(80), SpeedRPM(60))
            elif cs.reflected_light_intensity > 25:
                super().on(SpeedRPM(60), SpeedRPM(80))
        super().stop()

    def driveTillLine(self, cs):
        while cs.reflected_light_intensity > 25:
            if self.stop:
                super().stop()
                sys.exit()
                break
            super().on(self.speed, self.speed)
        super().stop()

    def driveTillFloor(self, cs):
        while cs.reflected_light_intensity < 25:
            if self.stop:
                super().stop()
                sys.exit()
                break
            super().on(self.speed, self.speed)
        super().stop()

    def driveTillBump(self, bumper):
        while True:
            if self.stop:
                super().stop()
                sys.exit()
                break
            super().on(self.speed, self.speed)
            if bumper.pressed_front():
                super().stop()
                sleep(0.2)
                break

#------------------
# our functions:
#------------------

def waitTillLights(state, cs):
    cs.mode = cs.MODE_COL_AMBIENT
    if state:
        while cs.ambient_light_intensity < 6:
            time.sleep(0.01)
            debug_print(cs.ambient_light_intensity)
    else:
        while cs.ambient_light_intensity >= 6:
            time.sleep(0.01)
            debug_print(cs.ambient_light_intensity)

    cs.mode = cs.MODE_COL_REFLECT

def back(speed):
    return speed * -1

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
        self.deg = 0 # 0 = open, 520 = closed

    def set_degrees(self, deg):
        self.deg = deg

    def close(self):
        super().on_for_degrees(SpeedRPM(-90), 520-self.deg)
        self.deg = 520

    def open(self):
        super().on_for_degrees(SpeedRPM(90), self.deg)
        self.deg = 0

    # 0% - open     100% - closed5
    def position(self, percent):
        super().on_for_degrees(SpeedRPM(90), self.deg-(percent * 5.2))
        self.deg = percent*5.2

#------------------
# Lift Class
#------------------
class Lifter(MediumMotor):
    def __init__(self, Port) -> None:
        super().__init__(Port)
        self.height = 3.6

    def move(self,cm):
        super().on_for_rotations(100,self.height_to_rotations(cm))
        self.height += cm

    def height_to_rotations(self, cm):
        return cm/3

    def move_to(self,cm):
        dif = cm - self.height
        super().on_for_rotations(100,self.height_to_rotations(dif))
        self.height = cm

    def init(self):
        self.move_to(3.6)
