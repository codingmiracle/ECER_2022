#!/usr/bin/env python3

import unittest
import os
import sys
import ev3dev2.led as ev3leds
import ev3dev2.sensor.lego as ev3sensors
import ev3dev2.sensor as ev3inputs
import ev3dev2.motor as ev3motors
import ev3dev2.wheel

from lib import *

# --- Functions ---



class Test(unittest.TestProgram):
    def __init__(self) -> None:
        self.attributes = "place here"
        self.bumper = Bumper(ev3inputs.INPUT_2, ev3inputs.INPUT_3)
        self.leds = ev3leds.Leds()

    def run(self):
        # set the console just how we want it
        set_cursor(OFF)
        self.loop()

    def loop(self):
        while True:
            if self.bumper.pressed_front():
                self.leds.set_color("LEFT", color="GREEN")
                self.leds.set_color("RIGHT", color="GREEN")
            elif self.bumper.pressed_right():
                self.leds.set_color("RIGHT", color="GREEN")
            elif self.bumper.pressed_left():
                self.leds.set_color("LEFT", color="GREEN")
            elif self.bumper.realesed():
                self.leds.set_color("LEFT", color="YELLOW")
                self.leds.set_color("RIGHT", color="YELLOW")
            else:
                self.leds.set_color("LEFT", color="RED")
                self.leds.set_color("RIGHT", color="RED")
            sleep(0.1)






if __name__ == '__main__':
    test = Test()
    test.run()
