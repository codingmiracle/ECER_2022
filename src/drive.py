#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.led import *

class DriveAdapter:

    def __init__(self, left, right) -> None:
        self.motor_l = LargeMotor(left)
        self.motor_r = LargeMotor(right)
        self.speed_l = 0
        self.speed_r = 0
        self.x = 0
        self.y = 0
        self.pathlist = []

    def set_speed(self, speedL, speedR):
        self.motor_l.duty_cycle_sp = speedL
        self.motor_r.duty_cycle_sp = speedR

    def drive_timed(self, time):
        self.motor_l.time_sp = time
        self.motor_r.time_sp = time

        self.motor_l.run_timed()
        self.motor_r.run_timed()
