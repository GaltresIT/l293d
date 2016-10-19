#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Load config
import config
verbose = config.verbose
test_mode = config.test_mode
pin_numbering = config.pin_numbering

# Print version
if verbose:
    import version
    print('L293D driver version ' + version.num)


# Import GPIO
try:
    import RPi.GPIO as GPIO
except Exception as e:
    print("Can't import RPi.GPIO. Please (re)install.")
    test_mode = True
    print('Test mode has been enabled. Please view README for more info.')
# Set GPIO warnings based on verbose value
if not test_mode:
    if verbose: GPIO.setwarnings(True)
    else: GPIO.setwarnings(False)


# Set GPIO mode
if not test_mode:
    if pin_numbering == 'BOARD':
        if verbose: print('Setting GPIO mode: BOARD')
        GPIO.setmode(GPIO.BOARD)
    elif pin_numbering == 'BCM':
        if verbose: print('Setting GPIO mode: BCM')
        GPIO.setmode(GPIO.BCM)
    else:
        print("pin_numbering must be either 'BOARD' or 'BCM'.")
        raise ValueError("pin_numbering must be either 'BOARD' or 'BCM'.")


# Import other modules used
from time import sleep
from threading import Thread


pins_in_use = [] # Lists pins in use (all motors)


class motor(object):
    """
    A motor wired to the L293D chip where
    motor_pins[0] is pinA is L293D pin1 or pin9  : On or off
    motor_pins[1] is pinB is L293D pin2 or pin10 : Anticlockwise positive
    motor_pins[2] is pinC is L293D pin7 or pin15 : Clockwise positive
    """
    
    # List of pins in use by motor object
    motor_pins = [0 for x in range(3)]

    def __init__(self, pinA=0, pinB=0, pinC=0):
        # Assign parameters to list
        self.motor_pins[0] = pinA
        self.motor_pins[1] = pinB
        self.motor_pins[2] = pinC
        
        # Check pins are valid
        self.pins_are_valid(self.motor_pins)
        # Append global list of pins in use
        pins_in_use.append(self.motor_pins)
        # Set up GPIO mode for pins
        self.gpio_setup(self.motor_pins)


    def pins_are_valid(self, pins, force_selection=False):
        global pin_numbering
        if pin_numbering == 'BOARD':
            valid_pins = [7, 11, 12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 36, 37]
        else: # 'BCM'
            valid_pins = [4, 5, 6, 12, 13, 16, 17, 18, 22, 23, 24, 25, 26, 27]
        for pin in pins:
            pin_int = int(pin)
            if (pin_int not in valid_pins) and (force_selection is not True):
                errStr =  ("GPIO pin number must be from list of valid pins: %s" 
                    "\nTo use selected pins anyway, set force_selection=True "
                    "in function call." % str(valid_pins))
                raise ValueError(errStr)
            for pin_in_use in pins_in_use:
                if pin_int in pin_in_use:
                    raise ValueError('GPIO pin {} already in use.'.format(pin_int))
        self.motor_pins = pins
        return True


    def gpio_setup(self, pins):
        for pin in pins:
            if not test_mode: GPIO.setup(pin, GPIO.OUT)


    def drive_motor(self, direction=1, duration=None, wait=True):
        if not test_mode:
            if (direction == 0):
                GPIO.output(self.motor_pins[0], GPIO.LOW)
            else:
                GPIO.output(self.motor_pins[direction], GPIO.HIGH)
                GPIO.output(self.motor_pins[direction*-1], GPIO.LOW)
                GPIO.output(self.motor_pins[0], GPIO.HIGH)
        if (duration is not None) and (direction != 0):
            stop_thread = Thread(target=self.stop, args = (duration, ))
            stop_thread.start()
            if wait:
                stop_thread.join()


    def pins_string_list(self):
        return '[{}, {} and {}]'.format(*self.motor_pins)


    def spin_clockwise(self, duration=None, wait=True):
        if verbose: print('spinning motor at {0} pins {1} clockwise.'.format(pin_numbering, self.pins_string_list()))
        self.drive_motor(direction=1, duration=duration, wait=wait)


    def spin_anticlockwise(self, duration=None, wait=True):
        if verbose: print('spinning motor at {0} pins {1} anticlockwise.'.format(pin_numbering, self.pins_string_list()))
        self.drive_motor(direction=-1, duration=duration, wait=wait)
    
    
    def clockwise(self, duration=None, wait=True):
        self.spin_clockwise(duration, wait)
    
    
    def anticlockwise(self, duration=None, wait=True):
        self.spin_anticlockwise(duration, wait)


    def stop(self, after=0):
        if after > 0: sleep(after)
        if verbose: print('stopping motor at {0} pins {1}.'.format(pin_numbering, self.pins_string_list()))
        if not test_mode: self.drive_motor(direction=0, duration=after, wait=True)


def cleanup():
    if not test_mode:
        try:
            GPIO.cleanup()
            if verbose: print('GPIO cleanup successful.')
        except:
            if verbose: print('GPIO cleanup failed.')
    else:
        if verbose: print('Cleanup not needed when test_mode is enabled.')

