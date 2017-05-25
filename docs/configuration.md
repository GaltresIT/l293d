# Configuration

The following config values can be changed after importing `l293d`.

## Test Mode:

Test mode (`test_mode`) is a paramter of the l293d config. By default it's off (False) although if there is a problem importing `RPi.GPIO` when `l293d.driver` is imported, test mode is enabled. You'll see something like the image below.

![l293d-import-test-mode](http://i.imgur.com/6aZnUiv.png?1)

_To change the value of `test_mode`, use `l293d.Config.set_test_mode(value)`, where value is True or False._

## Verbosity

Verbosity (`verbose`) is another True/False config value. l293d only prints textual output when `verbose` is True; which it is, by default.

The only thing that you should see as output from l293d when `verbose` is `False`, is when an exception is raised.

_To change the value of `verbose`, use `l293d.Config.set_verbose(value)`, where value is True or False._


## Pin Numbering

Pin numbering (`pin_numbering`) is either BOARD or BCM. These are different ways of numbering the Raspberry Pi's pins. BOARD numbering refers to the physical location of the pins, whereas BCM refers to the Broadcom pin number. A good pinout diagram labelling the pin & BCM numbers can be found at [pinout.xyz](https://pinout.xyz/).

_To change the value of `pin_numbering`, use `l293d.Config.set_pin_numbering(value)`, where value is either 'BOARD' or 'BCM'._

This value should only be changed before any motors have been defined. If you try to call `l293d.Config.set_pin_numbering` after defining a motor, an exception (`ValueError`) is raised.
