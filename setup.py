#!/usr/bin/env python
from info import version

from distutils.core import setup,Extension
setup(
    name = "l293d",
    version = version.num_string,
    author = "James Vickery",
    author_email = "jamesevickery.dev@gmail.com",
    description = ("A Python module to drive motors using an L293D via Raspberry Pi GPIO"),
    license = "MIT",
    keywords = "raspberry pi gpio l293d chip motor driver",
    url = "https://github.com/jamesevickery/l293d",
    packages=['l293d'],
)
