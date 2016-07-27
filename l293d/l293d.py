#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread

try:
    import RPi.GPIO as GPIO
except Exception as e:
    print('RPi.GPIO not installed.')
    test_mode = True
    print('Test mode has been enabled. Please view README for more info.')

if not test_mode:
    try:
        GPIO.setmode(GPIO.BOARD)
        if verbose: print('GPIO mode set (GPIO.BOARD)')
    except Exception as e:
        print('Can\'t set GPIO mode (GPIO.BOARD)')

verbose = True # Prints stuff to the terminal
test_mode = True # Disables GPIO calls when true
pins_in_use = []

class motor(object):
    """
    A motor wired to the L293D chip where
    motor_pins[0] is pinA is L293D pin1 or pin9  : On or off
    motor_pins[1] is pinB is L293D pin2 or pin10 : Anticlockwise positive
    motor_pins[2] is pinC is L293D pin7 or pin15 : Clockwise positive
    """
    
    motor_pins = [0 for x in range(3)]
    
    def __init__(self, pinA=0, pinB=0, pinC=0):
        self.pinA = pinA
        self.pinB = pinB
        self.pinC = pinC
        
        self.pins_are_valid(pinA, pinB, pinC)
        pins_in_use.append([pinA, pinB, pinC])
        self.gpio_setup(pinA, pinB, pinC)
    
    
    def pins_are_valid(self, pinA, pinB, pinC):
        pins = [pinA, pinB, pinC]
        for pin in pins:
            pin_int = int(pin)
            if (pin_int < 1) or (pin_int > 40):
                raise ValueError('GPIO pin number needs to be between 1 and 40 inclusively.')
            for motor in pins_in_use:
                if pin_int in motor:
                    raise ValueError('GPIO pin {} already in use.'.format(pin_int))
        self.motor_pins = pins
        return True
    
    
    def gpio_setup(self, A, B, C):
        for pin in [A, B, C]:
            if not test_mode: GPIO.setup(pin, GPIO.OUT)
    
        
    def spin(self, direction=1, duration=None, wait=True):
        if verbose: print('spinning motor at {} clockwise.'.format(self.pins_string_list()))
        # Code to start to spin motor (self) according to direction
        if duration is not None:
            stop_thread = Thread(target=self.stop, args = (duration, ))
            stop_thread.start()
            if wait:
                stop_thread.join()


    def pins_string_list(self):
        return '[{}, {} and {}]'.format(str(self.pinA), str(self.pinB), str(self.pinC))
    
    
    def spin_clockwise(self, duration=None, wait=True):
        self.spin(direction=1, duration=duration, wait=wait)
    
    
    def spin_anticlockwise(self, duration=None, wait=True):
        self.spin(direction=-1, duration=duration, wait=wait)
    
    
    def stop(self, after=0):
        if after > 0: sleep(after)
        if verbose: print('stopping {}.'.format(str(self)))


def cleanup():
    if not test_mode: GPIO.cleanup()
